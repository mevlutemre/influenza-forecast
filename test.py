import os

# __file__ o an çalışan scriptin adını ve yolunu verir.
# os.path.abspath bunu tam yola çevirir, dirname ise klasörünü ayıklar.
basepath = os.path.dirname(os.path.abspath(__file__))

print(f"{basepath}")
# Çıktı örn: /home/user/projects/my_project