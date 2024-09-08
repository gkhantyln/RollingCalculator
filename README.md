# Rolling Calculator

![Screen](screen.png)

## Genel Bakış

Rolling Calculator, spor bahislerinde kullanılmak üzere geliştirilmiş bir uygulamadır. Bu uygulama, bahis oranları, bahis tutarları, başlangıç kasası ve rolling sayısı gibi verileri girerek bahislerinizi yönetmenizi sağlar. Kazanç ve kayıpları takip eder, güncel kasa durumunu ve bahis tutarlarını hesaplar. Program ayrıca, veri girişini ve hesaplamaları kaydedip yüklemeyi destekler.

## Özellikler

- **Bahis Oranı**: Bahis oranını girin (örneğin, 2.0).
- **Başlangıç Bahis Tutarı**: İlk bahis tutarını belirtin.
- **Başlangıç Kasa**: İlk kasa miktarını girin.
- **Rolling Sayısı**: Toplam rolling sayısını belirtin.
- **Sabit/% Seçeneği**: Bahis tutarının hesaplanma yöntemini seçin:
  - **Sabit**: Güncel kasa miktarını belirli bir değere bölerek hesaplar.
  - **%**: Güncel kasa miktarının belirli bir yüzdesini kullanır.
- **Değer**: Sabit veya yüzdelik hesaplamada kullanılacak değer.

## Nasıl Çalışır?

1. **Giriş Yapın**: Bahis oranı, başlangıç bahis tutarı, başlangıç kasa miktarı, rolling sayısı ve seçenekler gibi bilgileri girin.
2. **Ekle**: "Ekle" butonuna basarak bahisleri tabloya ekleyin. Güncel kasa durumu, bahis tutarı ve olası kazanç hesaplanır.
3. **Raporu Kaydet**: Verileri ve hesaplamaları `conf_log.ini` dosyasına kaydedin.
4. **Raporu Yükle**: Daha önce kaydedilmiş raporu yükleyin ve verileri uygulamaya geri getirin.
5. **Temizle**: Tabloyu ve girilen değerleri temizleyin.

## Dosya Formatı

- **conf_log.ini**: Program tarafından kaydedilen ve yüklenen verileri içeren dosya. Bu dosya, bahis oranı, başlangıç tutarları, seçenekler ve tablodaki bahis sonuçlarını içerir.

## Kullanım

1. Programı açın ve gerekli alanları doldurun.
2. "Ekle" butonuna tıklayarak bahisleri ekleyin.
3. Hesaplamaları gözden geçirin ve gerekli düzenlemeleri yapın.
4. "Rapor Kaydet" butonuna tıklayarak verileri kaydedin veya "Temizle" butonuna tıklayarak tabloyu temizleyin.
5. Daha sonra tekrar çalıştırarak kaydedilmiş verileri yükleyin ve devam edin.

