from datetime import datetime
import os
import sys

# FILE SETTINGS

def makeSimplify(FilePath):
    # Start of Program
    DatasetPath         = "Dataset"
    ENV_PATH            = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FileName            = os.path.basename(FilePath)
    Name, _             = os.path.splitext(FileName)
    SimplifiedFilePath  = os.path.join(ENV_PATH, DatasetPath, Name + "_Simp.csv")
    CaseDict            = {}
    TotalRow            = 0
    ValidRecords        = 0

    print("[SIMP] Started...")

    with open(FilePath, mode="r", encoding="utf-8") as f:
        Headers         = f.readline().strip().split(",")
        DateID          = Headers.index("ISO_WEEKSTARTDATE")
        CaseID          = Headers.index("INF_ALL")
        
        for Row in f:
            TotalRow += 1
            Pieces = Row.strip().split(",")
            
            if len(Pieces) <= max(DateID, CaseID):
                continue
            
            DateText    = Pieces[DateID].strip()
            CaseRaw     = Pieces[CaseID].strip()
            
            if not DateText:
                continue
                
            try:
                DateObject = datetime.strptime(DateText, "%Y-%m-%d")
                DateSTD = DateObject.strftime("%Y-%m-%d")
                
                Case = int(float(CaseRaw)) if CaseRaw and CaseRaw != "NaN" else 0
                
                if JSON_Date := CaseDict.get(DateSTD):
                    CaseDict[DateSTD] += Case
                else:
                    CaseDict[DateSTD] = Case
                    
                ValidRecords += 1
            except Exception:
                continue

    SortedDates = sorted(CaseDict.keys())

    with open(SimplifiedFilePath, mode="w", encoding="utf-8") as f_out:
        f_out.write("date,count\n")
        
        for Date in SortedDates:
            f_out.write(f"{Date},{CaseDict[Date]}\n")

    print(f"[SIMP] Total row : {TotalRow}, total register : {ValidRecords}, total week count : {len(SortedDates)}")
    print(f"[SIMP] Final Dataset : {Name}")
    # End of Program

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: there is no file path arg!")
        print("Usage: python CSV_Simplifier.py [PATH]")
        exit()
    
    TargetPath = sys.argv[1]
    makeSimplify(TargetPath)