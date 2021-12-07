class YearConverter:
    regex = r"20\d{2}"
    
    def to_python(self, value): #문자열으 정수로 변경해서 넘겨줌
        return int(value)
    
    def to_url(self, value): #url 리버스할때 잘 리버싱 되도록 해주는 함수
        return "%04d" % value
    
class MonthConverter(YearConverter):
    regex = r"\d{1,2}"
    
class DayConverter(YearConverter):
    regex = r"[0123]\d"
    