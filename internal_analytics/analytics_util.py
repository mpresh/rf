from datetime import datetime, timedelta

def getChartLabel(temp_start, temp_end, splits, start, end):
    label = str(temp_start.month) + "/" + str(temp_start.day) + "-"
    label += str(temp_end.month) + "/" + str(temp_end.day) 
    return label
