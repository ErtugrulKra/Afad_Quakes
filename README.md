
# AFAD Quake Sensor

Bu Home Assistant sensörü, AFAD web sitesinden son depremleri çeker ve belirli bir büyüklüğün üzerindeki ilk depremi gösterir.

## Özellikler

- Büyüklük eşiği belirleme
- Google Maps bağlantısı
- 1 dakikalık yenileme

## Kurulum

1. `custom_components/afad_quake` klasörünü oluşturun.
2. Dosyaları bu klasöre kopyalayın.
3. `configuration.yaml` içine şunu ekleyin:
```yaml
sensor:
  - platform: afad_quake
    min_magnitude: 3.5
```
4. Home Assistant'ı yeniden başlatın.


Örnek CARD için Değerler

```markdown
**Büyüklük:** {{ state_attr('sensor.afad_son_deprem', 'buyukluk') }}

**Tarih:** {{ state_attr('sensor.afad_son_deprem', 'tarih') }}

**Enlem:** {{ state_attr('sensor.afad_son_deprem', 'enlem') }}

**Boylam:** {{ state_attr('sensor.afad_son_deprem', 'boylam') }}

**Derinlik:** {{ state_attr('sensor.afad_son_deprem', 'derinlik') }} km

**Tip:** {{ state_attr('sensor.afad_son_deprem', 'tip') }}

**Yer:** {{ state_attr('sensor.afad_son_deprem', 'yer') }}

[Harita Linki]( {{ state_attr('sensor.afad_son_deprem', 'harita') }} )
```