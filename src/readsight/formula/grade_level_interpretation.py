from __future__ import annotations


class GradeLevelInterpretation:
    @staticmethod
    def for_score(score: float) -> str:
        if score <= 1.0:
            return "Kindergarten"
        elif score <= 2.0:
            return "1st Grade"
        elif score <= 3.0:
            return "2nd Grade"
        elif score <= 4.0:
            return "3rd Grade"
        elif score <= 5.0:
            return "4th Grade"
        elif score <= 6.0:
            return "5th Grade"
        elif score <= 7.0:
            return "6th Grade"
        elif score <= 8.0:
            return "7th Grade"
        elif score <= 9.0:
            return "8th Grade"
        elif score <= 10.0:
            return "9th Grade"
        elif score <= 11.0:
            return "10th Grade"
        elif score <= 12.0:
            return "11th Grade"
        elif score <= 13.0:
            return "12th Grade"
        elif score <= 16.0:
            return "College"
        else:
            return "Graduate"
