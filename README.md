# Küresel Influenza Sinyallerinin Holt-Winters Öngörü Modeli ile Zaman Serisi Analizi



## CSV_Simplifer.py ile WHO FluNet ham verilerinin işlenmesi

```bash
python Tools/CSV_Simplifier.py <HamFluNet>
```

Bu kod ile WHOFluNet'den gelen ham verileri "Dataset" klasörünün içine sadeleştirip aktaran bir script.

## CSV_Visualizer.py ile Simp Verileri Görüntülenmesi

```bash
python Tools/CSV_Visualizer.py <SimpVeri>
```

Bu kod sadeleiştirilen ham verileri görselleştiren bir script.

## TrainAndTest.py

```bash
python TrainAndTest.py <SimpVeri>
```

Sadeleştirilen veri öğrenmeye girerek gelecek verileri oluşturur ve görselleştirir.