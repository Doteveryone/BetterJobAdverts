from jobcert import app

@app.template_filter('readability_words')
def readability_words_filter(s):
    score = int(s)
    if score in range(90, 100):
        return "Very Easy"
    elif score in range(80, 89):
        return "Easy"
    elif score in range(70, 79):
        return "Fairly Easy"
    elif score in range (60, 69):
        return "Standard"
    elif score in range (50, 59):    
        return "Fairly Difficult"
    elif score in range (30, 49):    
        return "Difficult"
    else:
        return "Very Confusing"

@app.template_filter('readability_status')
def readability_status_filter(s):
    score = int(s)
    if score in range(60, 100):
        return "success"
    elif score in range (30, 59):    
        return "warning"
    else:
        return "alert"

@app.template_filter('gender_coded_status')
def gender_coded_status_filter(s):
    if s in ('feminine-coded', 'strongly feminine-coded', 'neutral'):
        return "success"
    else:
        return "warning"