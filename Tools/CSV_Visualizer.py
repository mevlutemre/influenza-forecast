from datetime import datetime
import matplotlib.pyplot as plt
import sys

def visualize(CSVPath):
    DateList    = []
    Cases       = []

    print("[VISUAL] Started...")

    with open(CSVPath, mode = "r", encoding = "utf-8") as f:
        f.readline()
        
        for Row in f:
            Row = Row.strip()
            if not Row:
                continue
                
            Pieces = Row.split(",")
            DateText = Pieces[0]
            CaseText = Pieces[1]
            
            try:
                DateObj = datetime.strptime(DateText, "%Y-%m-%d")
                Case = int(CaseText)
                
                DateList.append(DateObj)
                Cases.append(Case)
            except Exception:
                continue

    print(f"[VISUAL] Total {len(DateList)} week datas ready...")

    TrendLine = []
    GraphSize = 52

    for i in range(len(Cases)):
        if i < GraphSize // 2 or i >=  len(Cases) - (GraphSize // 2):
            TrendLine.append(None)
        else:
            pencere = Cases[i - (GraphSize // 2) : i + (GraphSize // 2)]
            TrendLine.append(sum(pencere) / len(pencere))

    plt.figure(figsize = (14, 6))

    plt.plot(DateList, Cases, label = "Global Case Count", color = "#008080", alpha = 0.4, linewidth = 1.5)

    temiz_trend_x = [DateList[i] for i in range(len(TrendLine)) if TrendLine[i] is not None]
    temiz_trend_y = [TrendLine[i] for i in range(len(TrendLine)) if TrendLine[i] is not None]
    plt.plot(temiz_trend_x, temiz_trend_y, label = "52 Weekly Average", color = "#4B0082", linewidth = 2.5)

    plt.title("WHO FluNet - Worldwide Flu Graph", fontsize = 13, fontweight = 'bold')
    plt.xlabel("Years", fontsize = 11)
    plt.ylabel("Case Count", fontsize = 11)
    plt.legend(fontsize = 10)
    plt.grid(True, linestyle = ":", alpha = 0.5)

    plt.gcf().autofmt_xdate() 
    plt.tight_layout()

    plt.savefig("Raw_Data_Graph.png", dpi=600)
    plt.show()

if __name__  ==  "__main__":
    if len(sys.argv) < 2:
        print("Error: there is no file path arg!")
        print("Usage: python CSV_Visualizer.py [PATH]")
        exit()
    
    TargetPath = sys.argv[1]
    visualize(TargetPath)