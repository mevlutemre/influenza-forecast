from datetime import datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error
import sys

def train_and_test(CSV_PATH):

    DateList = []
    CaseList = []

    print("[TRAIN-TEST] Started...")

    with open(CSV_PATH, mode="r", encoding="utf-8") as f:
        f.readline()
        for Row in f:
            Row = Row.strip()
            if not Row: continue
            Pieces = Row.split(",")
            try:
                DateObj = datetime.strptime(Pieces[0], "%Y-%m-%d")
                Case = int(Pieces[1])
                DateList.append(DateObj)
                CaseList.append(Case)
            except:
                continue

    THRESHOLD_DATE = datetime(2020, 1, 1)

    TrainDate = [t for t in DateList if t < THRESHOLD_DATE]
    TrainCase = [CaseList[i] + 1 for i in range(len(DateList)) if DateList[i] < THRESHOLD_DATE]

    TestDate = [t for t in DateList if t >= THRESHOLD_DATE]
    TestCase = [CaseList[i] + 1 for i in range(len(DateList)) if DateList[i] >= THRESHOLD_DATE]

    print(f"[TRAIN-TEST] Train Dataset : {len(TrainCase)} week")
    print(f"[TRAIN-TEST] Test Dataset: {len(TestCase)} week")

    print("[TRAIN-TEST] Model training started!")
    Model = ExponentialSmoothing(TrainCase, 
                                trend="add", 
                                seasonal="mul", 
                                seasonal_periods=52).fit()

    Forecasts_ham = Model.forecast(len(TestCase))

    TrainCase_orj = [v - 1 for v in TrainCase]
    TestCase_orj = [v - 1 for v in TestCase]
    Forecasts = [max(0, t - 1) for t in Forecasts_ham]

    MAE = mean_absolute_error(TestCase_orj, Forecasts)
    print(f"[TRAIN-TEST] MAE for Pandemics: {MAE:.2f} Case")

    plt.figure(figsize=(14, 6))
    plt.plot(TrainDate, TrainCase_orj, label="Train Data", color="#008080", alpha=0.5)
    plt.plot(TestDate, TestCase_orj, label="Real Data", color="red", linewidth=2)
    plt.plot(TestDate, Forecasts, label="Prediction", color="darkorange", linestyle="--", linewidth=2.5)

    plt.title("Time Series Forecasting Model Results: Real Data and Forecasting", fontsize=13, fontweight='bold')
    plt.xlabel("Years")
    plt.ylabel("Weekly Case Count")
    plt.legend(fontsize=10)
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()

    # Save graph
    plt.savefig("Final_Graph.png", dpi=600)
    # print("[TRAIN-TEST] Graphics Saved: 'Final_Graph.png' ")
    plt.show()

if __name__  ==  "__main__":
    if len(sys.argv) < 2:
        print("Error: there is no file path arg!")
        print("Usage: python TrainAndTest.py [PATH]")
        exit()
    
    TargetPath = sys.argv[1]
    train_and_test(TargetPath)