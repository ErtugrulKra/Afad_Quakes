
# AFAD Quake Sensor

Bu Home Assistant sensörü, AFAD web sitesinden son depremleri çeker ve belirli bir büyüklüğün üzerindeki ilk depremi gösterir.

Sadece Marmara bölgesindeki 4 ve üzeri büyüklükteki depremler için çalışır hale getirildi.

## Kurulum

1. `custom_components/afad_quake` klasörünü oluşturun.
2. Dosyaları bu klasöre kopyalayın.
3. `configuration.yaml` içine şunu ekleyin:
```yaml

sensor:
  - platform: afad_quakes

```
4. Home Assistant'ı yeniden başlatın.


Örnek CARD için Değerler

```markdown
type: markdown
title: Deprem Durumu
content: >
  {% if states('sensor.marmara_depremi') not in ['unknown', 'unavailable', '',
  None] %} 
  **📍 Yer:** {{ state_attr('sensor.marmara_depremi', 'yer') }}  
  **📏 Büyüklük:** {{ states('sensor.marmara_depremi') }}  
  **🕒 Tarih:** {{ state_attr('sensor.marmara_depremi', 'tarih') }} 
  [Detay Sayfası Aç]( {{ state_attr('sensor.marmara_depremi', 'detay_link') }} )
  {% else %} 
  ✅ Güncel deprem yok.
  {% endif %}

```

Bildirim Otomasyonu 

```markdown
alias: Marmara Depremi
description: Marmara'da 4.0+ büyüklüğünde deprem bildirimi
triggers:
  - entity_id: sensor.marmara_depremi
    trigger: state
conditions:
  - condition: numeric_state
    entity_id: sensor.marmara_depremi
    above: 3.9
actions:
  - device_id: f682fxxxxxxxxxxxxxxxxxxxxxxxxxxx
    domain: mobile_app
    type: notify
    message: >-
      Marmara'da {{ state_attr('sensor.marmara_depremi', 'yer') }} bölgesinde {{
      states('sensor.marmara_depremi') }} büyüklüğünde deprem oldu ({{
      state_attr('sensor.marmara_depremi', 'tarih') }})
    title: Marmara da Deprem
  - device_id: ea2a8688129xxxxxxxxxxxxxxxxxxxxxxxxxx
    domain: mobile_app
    type: notify
    message: >-
      Marmara'da {{ state_attr('sensor.marmara_depremi', 'yer') }} bölgesinde {{
      states('sensor.marmara_depremi') }} büyüklüğünde deprem oldu ({{
      state_attr('sensor.marmara_depremi', 'tarih') }})
    title: Marmarada Deprem
mode: single


```
