from assessment.models import AssessmentAttempt
from assessment.models import (
    AssessmentAttempt,
    StudentAttributeScore,
)
from careers.models import Career, CareerAttributeWeight, CareerCourse
from colleges.models import CollegeCourse
from core.choices import EducationLevel,EDUCATION_ORDER





class CareerRecommendationService:

    def __init__(self, user):
        self.user = user
        self.student = user.student_profile
        self._latest_attempt = None
        self._student_scores = None



    def get_latest_attempt(self):

        if self._latest_attempt is None:

            self._latest_attempt = (
                AssessmentAttempt.objects.filter(
                    student=self.student,
                    is_completed=True,
                )
                .order_by("-completed_at")
                .first()
            )

        return self._latest_attempt
    


    def get_student_scores(self):
     attempt = self.get_latest_attempt()

     if not attempt:
        return []

     return (
        StudentAttributeScore.objects.filter(
            attempt=attempt,
        ).select_related("attribute")
    )


    def calculate_match_score(self, career,student_scores):

        #student_scores = self.get_student_scores()

        if not student_scores:
            return 0

        career_weights = {
            weight.attribute_id: weight
            for weight in career.attribute_weights.all()
        }

        total_score = 0
        total_weight = 0

        for student_score in student_scores:

            career_weight = career_weights.get(
                student_score.attribute_id
            )

            if not career_weight:
                continue

            total_score += (
                student_score.percentage
                * career_weight.weight
            )

            total_weight += career_weight.weight

        if total_weight == 0:
            return 0

        return round(total_score / total_weight, 2)
    




    def get_recommendations(self):
        recommendations = []

        careers =( Career.objects.filter(
            is_active=True,
        )
        . prefetch_related(
            "attribute_weights__attribute",
            "career_courses__course",
        )
        )

        student_scores = self.get_student_scores()

        for career in careers:

            match_score = self.calculate_match_score(career, student_scores)

            eligible = self.is_eligible(career)

            recommendations.append(
               self.build_recommendation(
                  career,
                  match_score,
                  eligible
                  
               )
            )

        recommendations.sort(
            key=lambda x: x["match_score"],
            reverse=True,
        )

        for rank, recommendation in enumerate(
            recommendations,
            start=1,
        ):
            recommendation["rank"] = rank

        return recommendations
    



    def is_eligible(self, career):
     student_level = EDUCATION_ORDER.get(
        self.student.highest_education_level,
        0,
    )

     career_level = EDUCATION_ORDER.get(
        career.minimum_education_level,
        0,
    )

     return student_level >= career_level
    


    def get_next_step(self, career,eligible):

     student_level = self.student.highest_education_level
     career_level = career.minimum_education_level

     if eligible:
        return "You meet the minimum education requirement."

     if (
        student_level == EducationLevel.SEE
        and career_level == EducationLevel.BACHELOR
     ):
        return "Complete +2 and then enroll in a Bachelor's degree."

     if (
        student_level == EducationLevel.PLUS_TWO
        and career_level == EducationLevel.BACHELOR
     ):
        return "Enroll in a Bachelor's degree."

     if (
        student_level == EducationLevel.DIPLOMA
        and career_level == EducationLevel.BACHELOR
     ):
        return "Complete or bridge to a Bachelor's degree."

     return "Complete the required education level."
    


    def get_recommended_courses(self, career):

     career_courses = (
        CareerCourse.objects.filter(
            career=career,
        )
        .select_related("course")
        .order_by("-is_primary", "course__name")
     )

     courses = []

     for career_course in career_courses:

        courses.append(
            {
                "id": career_course.course.id,
                "name": career_course.course.name,
                "short_name": career_course.course.short_name,
                "is_primary": career_course.is_primary,
            }
        )

     return courses
    

    def build_recommendation(
        self,
        career,
        match_score,
        eligible,
        ):

        return {
            "career": career,
            "match_score": match_score,
            "eligible": eligible,
            
            "minimum_education_level": career.minimum_education_level,
            "recommended_courses": self.get_recommended_courses(career),
           "top_colleges": self.get_top_colleges(career),
            "next_step": self.get_next_step(
                career,
                eligible,
            ),
        }
    


    def get_top_colleges(self, career):

        course_ids = (
            CareerCourse.objects.filter(
                career=career,
            )
            .values_list(
                "course_id",
                flat=True,
            )
        )

        college_courses = (
            CollegeCourse.objects.filter(
                course_id__in=course_ids,
                is_available=True,
                college__is_active=True,
            )
            .select_related(
                "college",
                "college__province",
                "college__district",
            )
            
        )

        unique_colleges = {}

        # colleges = []

        for college_course in college_courses:
            college = college_course.college
            if college.id not in unique_colleges:

                unique_colleges[college.id]=  {
                        "id": college_course.college.id,
                        "name": college_course.college.name,
                        "province": college_course.college.province.name,
                        "district": college_course.college.district.name,
                        "address": college_course.college.address,
                    }
            

        return list(unique_colleges.values())[:5]