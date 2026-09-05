BEGIN TRANSACTION;
CREATE TABLE "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);
CREATE TABLE "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);
INSERT INTO "auth_permission" VALUES(1,1,'add_logentry','Can add log entry');
INSERT INTO "auth_permission" VALUES(2,1,'change_logentry','Can change log entry');
INSERT INTO "auth_permission" VALUES(3,1,'delete_logentry','Can delete log entry');
INSERT INTO "auth_permission" VALUES(4,1,'view_logentry','Can view log entry');
INSERT INTO "auth_permission" VALUES(5,2,'add_permission','Can add permission');
INSERT INTO "auth_permission" VALUES(6,2,'change_permission','Can change permission');
INSERT INTO "auth_permission" VALUES(7,2,'delete_permission','Can delete permission');
INSERT INTO "auth_permission" VALUES(8,2,'view_permission','Can view permission');
INSERT INTO "auth_permission" VALUES(9,3,'add_group','Can add group');
INSERT INTO "auth_permission" VALUES(10,3,'change_group','Can change group');
INSERT INTO "auth_permission" VALUES(11,3,'delete_group','Can delete group');
INSERT INTO "auth_permission" VALUES(12,3,'view_group','Can view group');
INSERT INTO "auth_permission" VALUES(13,4,'add_user','Can add user');
INSERT INTO "auth_permission" VALUES(14,4,'change_user','Can change user');
INSERT INTO "auth_permission" VALUES(15,4,'delete_user','Can delete user');
INSERT INTO "auth_permission" VALUES(16,4,'view_user','Can view user');
INSERT INTO "auth_permission" VALUES(17,5,'add_contenttype','Can add content type');
INSERT INTO "auth_permission" VALUES(18,5,'change_contenttype','Can change content type');
INSERT INTO "auth_permission" VALUES(19,5,'delete_contenttype','Can delete content type');
INSERT INTO "auth_permission" VALUES(20,5,'view_contenttype','Can view content type');
INSERT INTO "auth_permission" VALUES(21,6,'add_session','Can add session');
INSERT INTO "auth_permission" VALUES(22,6,'change_session','Can change session');
INSERT INTO "auth_permission" VALUES(23,6,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES(24,6,'view_session','Can view session');
INSERT INTO "auth_permission" VALUES(25,7,'add_product','Can add product');
INSERT INTO "auth_permission" VALUES(26,7,'change_product','Can change product');
INSERT INTO "auth_permission" VALUES(27,7,'delete_product','Can delete product');
INSERT INTO "auth_permission" VALUES(28,7,'view_product','Can view product');
INSERT INTO "auth_permission" VALUES(29,8,'add_service','Can add service');
INSERT INTO "auth_permission" VALUES(30,8,'change_service','Can change service');
INSERT INTO "auth_permission" VALUES(31,8,'delete_service','Can delete service');
INSERT INTO "auth_permission" VALUES(32,8,'view_service','Can view service');
INSERT INTO "auth_permission" VALUES(33,9,'add_sitesettings','Can add Site Settings');
INSERT INTO "auth_permission" VALUES(34,9,'change_sitesettings','Can change Site Settings');
INSERT INTO "auth_permission" VALUES(35,9,'delete_sitesettings','Can delete Site Settings');
INSERT INTO "auth_permission" VALUES(36,9,'view_sitesettings','Can view Site Settings');
INSERT INTO "auth_permission" VALUES(37,10,'add_socialmedia','Can add social media');
INSERT INTO "auth_permission" VALUES(38,10,'change_socialmedia','Can change social media');
INSERT INTO "auth_permission" VALUES(39,10,'delete_socialmedia','Can delete social media');
INSERT INTO "auth_permission" VALUES(40,10,'view_socialmedia','Can view social media');
INSERT INTO "auth_permission" VALUES(41,11,'add_whatsapptemplate','Can add WhatsApp Template');
INSERT INTO "auth_permission" VALUES(42,11,'change_whatsapptemplate','Can change WhatsApp Template');
INSERT INTO "auth_permission" VALUES(43,11,'delete_whatsapptemplate','Can delete WhatsApp Template');
INSERT INTO "auth_permission" VALUES(44,11,'view_whatsapptemplate','Can view WhatsApp Template');
INSERT INTO "auth_permission" VALUES(45,12,'add_userprofile','Can add user profile');
INSERT INTO "auth_permission" VALUES(46,12,'change_userprofile','Can change user profile');
INSERT INTO "auth_permission" VALUES(47,12,'delete_userprofile','Can delete user profile');
INSERT INTO "auth_permission" VALUES(48,12,'view_userprofile','Can view user profile');
INSERT INTO "auth_permission" VALUES(49,13,'add_productimage','Can add product image');
INSERT INTO "auth_permission" VALUES(50,13,'change_productimage','Can change product image');
INSERT INTO "auth_permission" VALUES(51,13,'delete_productimage','Can delete product image');
INSERT INTO "auth_permission" VALUES(52,13,'view_productimage','Can view product image');
CREATE TABLE "auth_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "first_name" varchar(150) NOT NULL);
INSERT INTO "auth_user" VALUES(2,'pbkdf2_sha256$1000000$fY3cYs3uP1XynXq4bj4Is6$lJqFi6VGSujCB1H1J/2bDD4tx2RJGHqNsug/CF9ry6E=','2025-12-25 03:21:19.911330',1,'eka','','eka@gmail.com',1,1,'2025-08-03 09:15:18.748330','');
CREATE TABLE "auth_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "auth_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "core_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL, "description" text NOT NULL, "image" varchar(100) NOT NULL, "price" decimal NOT NULL, "discount_price" decimal NULL, "link_label" varchar(50) NOT NULL, "additional_link" varchar(255) NULL, "additional_link_label" varchar(50) NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "link" varchar(255) NULL);
INSERT INTO "core_product" VALUES(32,'Jasa Trial Canva Pro 30 Hari','🎨 Nikmati Semua Fitur Premium Canva Pro Secara Gratis Selama 30 Hari! 💥','products/id-11134207-7r98q-ltijzawe7h4o4d.webp',150000,5000,'Link Pembelian',NULL,'',1,'2025-08-12 12:06:28.286208','2025-08-12 12:09:27.022547','https://clicky.id/redirect/promo-page?product=689b296c3ab93717be6c1dac');
INSERT INTO "core_product" VALUES(33,'Biolinkku: Template Bio Link & Dashboard Admin','Biolinkku" adalah template website bio link modern yang responsif dan mudah dimodifikasi, dibuat dengan kombinasi Django sebagai backend yang andal dan Tailwind CSS untuk desain frontend yang fleksibel. Template ini dirancang khusus untuk para kreator, pengusaha, atau siapa pun yang ingin mengelola semua tautan penting mereka di satu tempat.','products/Macbook-Air-biolinkku_nqTewle.my.id.png',350000,99999,'Beli Sekarang',NULL,'',1,'2025-08-12 12:14:17.480078','2025-08-12 12:14:17.480128','https://clicky.id/redirect/promo-page?product=689b296c3ab93717be6c1dac');
INSERT INTO "core_product" VALUES(34,'2200++ VIDEO KONTEN WISATA - Video Konten Viral Siap Upload','Dapatkan koleksi super lengkap berisi lebih dari 2200 video konten wisata viral, siap Anda upload langsung ke media sosial Anda! Tidak perlu repot syuting, editing, atau mencari ide. Semua video sudah dikurasi dan dijamin berkualitas tinggi, sempurna untuk meningkatkan engagement di akun TikTok, Instagram Reels, atau YouTube Shorts Anda. Dengan akses seumur hidup, Anda bisa menggunakannya kapan pun, tanpa batas. Cukup unduh, unggah, dan saksikan akun Anda berkembang pesat.','products/id-11134207-7rbk1-m7e2bfqbm4g617.webp',25000,5000,'link pembelian',NULL,'',1,'2025-08-12 12:25:19.610444','2025-08-12 12:25:19.610488','http://lynk.id/affiliatepemula/1o6wnd9/checkout');
INSERT INTO "core_product" VALUES(35,'1000+ SOURCE CODE PHP MySQL (Siap Pakai)','Miliki koleksi terlengkap 1000+ source code program aplikasi sistem informasi berbasis web, siap pakai, dan bisa dikembangkan. Sangat ideal untuk tugas kuliah, belajar pemrograman, atau proyek pribadi. Dapatkan akses seumur hidup ke semua file project PHP CodeIgniter dan Laravel. Hemat waktu dan selesaikan proyek Anda dengan cepat!

PENTING!

Produk ini adalah file source code, bukan aplikasi siap pakai. Pembeli harus memiliki pengetahuan dasar PHP, MySQL, dan cara instalasi di XAMPP/WAMP. Kami tidak menyediakan layanan bantuan teknis.','products/id-11134207-7ra0i-mbg70muci45s3c.webp',150000,15000,'Beli sekarang',NULL,'',1,'2025-08-13 07:26:12.026118','2025-08-13 07:26:50.278749','http://lynk.id/affiliatepemula/l5rxnj47p69q/checkout');
INSERT INTO "core_product" VALUES(36,'Animal Alphabet Vector Set','UDAYAKAN MEMBACA DESKRIPSI PRODUK GESER FOTO/VIDEO HINGGA SELESAI YAH!!



INFO

• Produk ini digital tidak ada bentuk fisik.

• Semua produk ditoko ini sudah dikategorikan/disusun kedalam etalase,



CARA ORDER

• Chekout Produk Yang Sudah Di List

• Cantumkan Gmail di Note Pemesanan

• Seller Mengirimkan File Pembelian

• Seller Konfirmasi Produk Sudah Dikirim','products/dsd.webp',10000,1000,'Beli Sekarang',NULL,'',1,'2025-08-13 07:34:43.836028','2025-08-13 07:38:21.780665','http://lynk.id/affiliatepemula/qdx8ZZ2/checkout');
INSERT INTO "core_product" VALUES(37,'photo collage frame effect mockup','IAP PAKAI DAN SIAP EDIT / EDITABLE PHOTOSOP (PSD) DESAIN EDITABLE ARTINYA BUKAN DESAIN MATI, MUDAH DIEDIT SENDIRI DAN BISA DI UTAK-ATIK, SEHINGGA MENGHEMAT WAKTU DAN BIAYA ANDA, DESAIN TERKINI YANG SESUAI SELERA PASAR SAAT INI','products/Cuplikan_layar_2025-08-13_144052.png',5000,500,'Beli Sekarang',NULL,'',1,'2025-08-13 07:44:27.331137','2025-08-13 07:44:27.331184','http://lynk.id/affiliatepemula/8mDYOoe/checkout');
INSERT INTO "core_product" VALUES(38,'Alphabet Art Vector Set CorelDraw','Detail Item:  

Alphabet Art Vector Set – Koleksi Desain Vektor Huruf  



• Koleksi desain vektor berkualitas tinggi bertema seni huruf, ideal untuk berbagai kebutuhan kreatif dan desain grafis.  



Spesifikasi Produk:  

• Total Item: Sesuai jumlah pada gambar pratinjau postingan.  

• Format File: CorelDRAW X7.  

• Real Vector:  

  - Desain berbasis vektor yang memberikan hasil tajam tanpa kehilangan kualitas.  

• Kustomisasi Penuh:  

  - Warna dan ukuran dapat diedit sesuai kebutuhan desain Anda.  

• Mode Warna: CMYK, ideal untuk menghasilkan cetakan berkualitas profesional.  

• Kegunaan:  

  - Branding merchandise dengan desain huruf yang unik dan kreatif.  

  - Proyek desain seperti poster, undangan, atau dekorasi.  

  - Media cetak atau digital dengan elemen seni huruf yang menarik.','products/sg-11134201-7qvfo-ljn8wuvxyg6j23.webp',15000,2500,'Beli Sekarang','http://lynk.id/affiliatepemula/Bmq830k','Product Detail',1,'2025-08-13 07:54:59.408698','2025-08-13 07:58:25.384132','http://lynk.id/affiliatepemula/Bmq830k/checkout');
INSERT INTO "core_product" VALUES(39,'3d Cartoon Text Effects','Features:



10 PSD Files

2000×1500px

300dpi RGB

Fully Editable

Well organised

Smart object layers

Help file','products/sg-11134201-7qvcx-lfa0k2qifben88.webp',25000,2500,'Beli Sekarang',NULL,'',1,'2025-08-13 08:07:59.275066','2025-08-13 08:07:59.275104','http://lynk.id/affiliatepemula/Q2KYqak/checkout');
INSERT INTO "core_product" VALUES(40,'1300 Wedding Cards In CorelDraw Files','1300 Wedding Cards In CDR Files



Product Specs

Compatible with: CorelDraw X7 or Up

File Type : Cdr

1300 : Cdr

Vector 100%

Size Compressed 2GB','products/sg-11134201-7qveq-ljn740z9cjmz06.webp',10000,5000,'Beli Sekarang',NULL,'',1,'2025-08-13 08:15:56.445596','2025-08-13 08:15:56.445642','http://lynk.id/affiliatepemula/a7kvqbK/checkout');
INSERT INTO "core_product" VALUES(41,'45 Photo Collage Print Template','Produk ini digital tidak ada bentuk fisik.

Semua produk ditoko ini selalu ready ya kak!!


CARA ORDER


Chekout Produk Yang Sudah Di List

Cantumkan Gmail di Note Pemesanan

Seller Mengirimkan File Pembelian

Seller Konfirmasi Produk Sudah Dikirim


FITUR


100% Gratis Ongkir

Akses Download G-Drive

File Terkompress Maksimal

Full Support

Bonus Exclusive


Yang Akan Anda Dapatkan


15 Photo Collage Ai Lanscape

35 Photo Collage Ai Portrait

15 Photo Collage PS Lanscape

35 Photo Collage PS Portrait

45 JPG Preview

45 JPG MockUp


PRODUCT SPECS


• 45 Photo Collage Print Template

• Sudah Termasuk Mockup (Front Only)

• Tidak Termasuk Tutorial

• Warna Dapat di Edit

• Font Dapat di Edit

• Ukuran Dapat di Edit


BISA DI EDIT DI APLIKASI


04 - Versi Illustrator 25.0 (ai)

07 - Versi Photoshop CC 2014 (psd)','products/sg-11134201-7qve6-lfa0gl8a4lqgda.webp',10000,3000,'Beli Sekarang','http://lynk.id/affiliatepemula/E4Era5L','Detail Product',1,'2025-08-13 08:26:17.008713','2025-08-13 08:26:17.008772','http://lynk.id/affiliatepemula/E4Era5L/checkout');
INSERT INTO "core_product" VALUES(42,'Jasa Unduh Envato Elements Termurah dan Tercepat','Dapatkan 10 unduhan Envato Elements hanya dengan Rp10.000! Layanan kami menawarkan harga termurah dan proses tercepat.','products/Cuplikan_layar_2025-08-13_153345.png',50000,10000,'Beli Sekarang','https://wa.me/6282392115909?text=Halo%2C%20saya%20ingin%20bertanya%20tentang%20Jasa%20Unduh%20Envato%20Elements%20Termurah%20dan%20Tercepat','Pertanyaan',1,'2025-08-13 08:40:40.444038','2025-08-13 08:40:40.444079','http://lynk.id/affiliatepemula/ov177j9ewgyd/checkout');
INSERT INTO "core_product" VALUES(43,'100+ T-Shirt Sticker Bombs Vector CorelDraw','96 T-Shirt Sticker Bombs Vector – Koleksi Desain Stiker T-Shirt


• Koleksi desain vektor berkualitas tinggi bertema stiker untuk T-Shirt, dirancang untuk berbagai kebutuhan kreatif Anda.


Spesifikasi Produk:

• Total Item: 96 desain sesuai jumlah pada gambar pratinjau postingan.

• Format File: CorelDRAW X7.

• Real Vector:

- Desain berbasis vektor yang memberikan hasil tajam tanpa kehilangan kualitas.

• Kustomisasi Penuh:

- Warna dan ukuran dapat diedit sesuai kebutuhan desain Anda.

• Mode Warna: CMYK, ideal untuk menghasilkan cetakan berkualitas profesional.

• Kegunaan:

- Branding merchandise unik bertema stiker T-Shirt.

- Proyek desain kreatif seperti poster, undangan, atau dekorasi.

- Media cetak atau digital dengan elemen desain stiker yang menarik dan inovatif.


INFO:

• Produk ini digital, tidak ada bentuk fisik.

• File dikirim via Gmail setelah pembelian.

• Kategori Produk: Semua item telah diorganisir dalam etalase untuk mempermudah pencarian.


Fitur Utama:

• 100% Gratis Ongkir: Tanpa biaya tambahan untuk pengiriman produk digital.

• Akses Download G-Drive: File tersedia untuk unduhan langsung melalui Google Drive.

• File Terkompresi Maksimal: Memastikan efisiensi penyimpanan dan transfer file.

• Full Support: Bantuan penuh dari penjual untuk memastikan pengalaman pembeli yang memuaskan.

• Bonus Eksklusif: Hadiah menarik untuk pembeli setia.


Cara Order:

• Pilih produk dari daftar etalase yang tersedia.

• Cantumkan Gmail Anda di catatan pesanan.

• File pembelian akan dikirimkan langsung ke email Anda.

• Penjual akan mengonfirmasi pengiriman produk selesai.


Tags:

#StickerBombsVector #ProdukDigital #CorelDRAWX7 #EditableVectors #CMYKColor #CreativeTShirtDesignAssets','products/c60ccb277c993601c4e4952854115609.webp',30000,3000,'Beli Sekarang','http://lynk.id/affiliatepemula/lxv55ezvyzv5','Product Detail',1,'2025-08-13 09:16:08.898380','2025-08-13 09:16:08.898423','http://lynk.id/affiliatepemula/lxv55ezvyzv5/checkout');
CREATE TABLE "core_productimage" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "image" varchar(100) NOT NULL, "order" integer NOT NULL, "created_at" datetime NOT NULL, "product_id" bigint NOT NULL REFERENCES "core_product" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "core_productimage" VALUES(6,'products/id-11134207-7r98r-ltijzawe8vp4bd.webp',2,'2025-08-12 12:09:00.840340',32);
INSERT INTO "core_productimage" VALUES(7,'products/xf.png',1,'2025-08-12 12:14:17.686127',33);
INSERT INTO "core_productimage" VALUES(8,'products/Macbook-Air-biolinkku.my.id_4.png',2,'2025-08-12 12:14:17.830788',33);
INSERT INTO "core_productimage" VALUES(9,'products/Macbook-Air-biolinkku.my.id_3.png',3,'2025-08-12 12:14:17.974028',33);
INSERT INTO "core_productimage" VALUES(10,'products/dss.png',4,'2025-08-12 12:14:18.058200',33);
INSERT INTO "core_productimage" VALUES(11,'products/dfd.png',5,'2025-08-12 12:14:18.130579',33);
INSERT INTO "core_productimage" VALUES(12,'products/as.png',6,'2025-08-12 12:14:18.256385',33);
INSERT INTO "core_productimage" VALUES(13,'products/Macbook-Air-biolinkku_v24CL1O.my.id_2.png',7,'2025-08-12 12:14:18.357533',33);
INSERT INTO "core_productimage" VALUES(14,'products/Macbook-Air-biolinkku_HSaRsZd.my.id_1.png',8,'2025-08-12 12:14:18.546867',33);
INSERT INTO "core_productimage" VALUES(15,'products/id-11134207-7rbk6-m72jiaeebeefef.webp',1,'2025-08-12 12:25:20.313145',34);
INSERT INTO "core_productimage" VALUES(16,'products/id-11134207-7ra0q-mbg70mucgplcd8.webp',1,'2025-08-13 07:26:12.127613',35);
INSERT INTO "core_productimage" VALUES(17,'products/22148eac9c0d2a14e8270f2dd837fb7d.webp',1,'2025-08-13 07:34:43.979908',36);
INSERT INTO "core_productimage" VALUES(18,'products/8057af731cfceec3afb031b704adec85.webp',2,'2025-08-13 07:34:44.134549',36);
INSERT INTO "core_productimage" VALUES(19,'products/sg-11134201-22100-s7hmx0d85jivf3.webp',3,'2025-08-13 07:34:44.396101',36);
INSERT INTO "core_productimage" VALUES(20,'products/097ec74e89f383498077186a86477915.webp',4,'2025-08-13 07:34:44.524205',36);
INSERT INTO "core_productimage" VALUES(21,'products/097ec74e89f383498077186a86477915_1.webp',5,'2025-08-13 07:34:44.649598',36);
INSERT INTO "core_productimage" VALUES(22,'products/Cuplikan_layar_2025-08-13_144059.png',1,'2025-08-13 07:44:27.458220',37);
INSERT INTO "core_productimage" VALUES(23,'products/bbc7798ad87b6363498c1a1ce2f80815.webp',1,'2025-08-13 07:54:59.512843',38);
INSERT INTO "core_productimage" VALUES(24,'products/0fcdf8cd7c040db540ae06198aef8011.webp',2,'2025-08-13 07:54:59.721848',38);
INSERT INTO "core_productimage" VALUES(25,'products/3da9726bf64399b30d95ea0331856594.webp',3,'2025-08-13 07:54:59.878919',38);
INSERT INTO "core_productimage" VALUES(26,'products/689e849634f32540cb89a60cbba70d9b.webp',4,'2025-08-13 07:54:59.960951',38);
INSERT INTO "core_productimage" VALUES(27,'products/103e7684e9fc2751b63cb565e7e98fa0.webp',5,'2025-08-13 07:55:00.032150',38);
INSERT INTO "core_productimage" VALUES(28,'products/sg-11134201-22120-bci4ezl3g7kv7c.webp',1,'2025-08-13 08:07:59.430571',39);
INSERT INTO "core_productimage" VALUES(29,'products/sg-11134201-22120-www5ezl3g7kva2.webp',2,'2025-08-13 08:08:00.324508',39);
INSERT INTO "core_productimage" VALUES(30,'products/sg-11134201-22120-uib65yl3g7kv6d.webp',3,'2025-08-13 08:08:00.412989',39);
INSERT INTO "core_productimage" VALUES(31,'products/sg-11134201-22120-qll09ul3g7kv58.webp',4,'2025-08-13 08:08:00.484298',39);
INSERT INTO "core_productimage" VALUES(32,'products/sg-11134201-22120-81qjbol3g7kv3d.webp',5,'2025-08-13 08:08:00.648906',39);
INSERT INTO "core_productimage" VALUES(33,'products/sg-11134201-22120-i8wii9bis7kvae.webp',1,'2025-08-13 08:15:56.563033',40);
INSERT INTO "core_productimage" VALUES(34,'products/sg-11134201-22120-cgt3wubis7kv3b.webp',2,'2025-08-13 08:15:56.699871',40);
INSERT INTO "core_productimage" VALUES(35,'products/sg-11134201-22120-3gz5t5ais7kv22.webp',3,'2025-08-13 08:15:56.833359',40);
INSERT INTO "core_productimage" VALUES(36,'products/sg-11134201-22120-xhddpnbis7kvc3.webp',4,'2025-08-13 08:15:56.929843',40);
INSERT INTO "core_productimage" VALUES(37,'products/sg-11134201-22120-eigwnabis7kvb6.webp',5,'2025-08-13 08:15:57.022772',40);
INSERT INTO "core_productimage" VALUES(38,'products/sg-11134201-22120-u0nfqacis7kv1e.webp',6,'2025-08-13 08:15:57.112485',40);
INSERT INTO "core_productimage" VALUES(39,'products/sg-11134201-22120-i2turbbis7kvae.webp',7,'2025-08-13 08:15:57.200087',40);
INSERT INTO "core_productimage" VALUES(40,'products/sg-11134201-22120-3fxd5u7hs7kv6b.webp',8,'2025-08-13 08:15:57.401864',40);
INSERT INTO "core_productimage" VALUES(41,'products/sg-11134201-7qvfb-lf9pc8jxanop42.webp',1,'2025-08-13 08:26:17.100566',41);
INSERT INTO "core_productimage" VALUES(42,'products/sg-11134201-7qvel-lf9pc8edis15fb.webp',2,'2025-08-13 08:26:17.184852',41);
INSERT INTO "core_productimage" VALUES(43,'products/sg-11134201-7qvg2-lf9pc86lvja089.webp',3,'2025-08-13 08:26:17.265703',41);
INSERT INTO "core_productimage" VALUES(44,'products/sg-11134201-7qvdm-lf9pc81m2uge42.webp',4,'2025-08-13 08:26:17.337510',41);
INSERT INTO "core_productimage" VALUES(45,'products/sg-11134201-7qvdv-lf9pc7uoblf370.webp',5,'2025-08-13 08:26:17.419599',41);
INSERT INTO "core_productimage" VALUES(46,'products/sg-11134201-7qvcx-lf9pc7ngm5pv9d.webp',6,'2025-08-13 08:26:17.525102',41);
INSERT INTO "core_productimage" VALUES(47,'products/sg-11134201-7qve5-lf9pc7jkru5yac.webp',7,'2025-08-13 08:26:17.615716',41);
INSERT INTO "core_productimage" VALUES(48,'products/sg-11134201-7qvek-ljn6tb6rwn4i44.webp',8,'2025-08-13 08:26:17.704850',41);
INSERT INTO "core_productimage" VALUES(49,'products/43532b6fd4feae6d6ed3fd0450404876.webp',1,'2025-08-13 09:16:09.032347',43);
INSERT INTO "core_productimage" VALUES(50,'products/adfe5cea191b22c312ce148ffc2f0f13.webp',2,'2025-08-13 09:16:09.160375',43);
INSERT INTO "core_productimage" VALUES(51,'products/504680a8d14192c9f31c6dcf0c6181be.webp',3,'2025-08-13 09:16:09.287660',43);
CREATE TABLE "core_service" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL, "description" text NOT NULL, "icon" varchar(100) NOT NULL, "link" varchar(200) NULL, "color" varchar(50) NOT NULL, "gradient_color" varchar(50) NULL, "gradient_type" varchar(20) NOT NULL, "gradient_direction" varchar(20) NOT NULL, "order" integer NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
INSERT INTO "core_service" VALUES(3,'PowerPoint Morph Template','Template Presentasi Keren dengan Morph','services/MAHIRPPT.png','https://clicky.id/arifex21','#ac4602','#e6891e','linear','to bottom left',0,1,'2025-07-28 13:40:29.584656','2025-08-03 09:55:03.834838');
INSERT INTO "core_service" VALUES(4,'Gudang File Digital Komplit','Mau cari file digital apa saja? Kami punya solusinya!','services/Gemini_Generated_Image_g7qp0ug7qp0ug7qp.png','https://lynk.id/affiliatepemula','#ef4444','#dc2626','linear','to right',0,1,'2025-07-28 13:40:29.591197','2025-08-03 09:55:23.395664');
INSERT INTO "core_service" VALUES(5,'Temukan Barang Unik di Sini!','koleksi barang unik, aesthetic, dan langka','services/ChatGPT_Image_Jun_19_2025_07_23_59_PM.png','https://oliviafadillah23.passio.eco/','#8b5cf6','#7c3aed','linear','to right',0,1,'2025-07-28 13:40:29.597987','2025-08-03 09:55:39.149299');
INSERT INTO "core_service" VALUES(6,'Koleksi Template Website','Template website premium dengan desain modern, responsif,','services/ChatGPT_Image_Jun_19_2025_07_19_56_PM.png','https://lynk.id/affiliatepemula','#06b6d4','#0891b2','linear','to right',0,1,'2025-07-28 13:40:29.604482','2025-08-03 09:56:04.763013');
INSERT INTO "core_service" VALUES(7,'Template Portofolio','Tingkatkan karir Anda dengan template portofolio premium. Desain modern','services/ChatGPT_Image_Aug_3_2025_02_45_28_PM.png','https://clicky.id/arifex21','#ec4899','#db2777','linear','to right',0,1,'2025-07-28 13:40:29.610723','2025-08-12 13:29:41.372514');
INSERT INTO "core_service" VALUES(10,'Donasi & Support','Dukung pengembangan template gratis dengan donasi','services/ChatGPT_Image_Aug_3_2025_02_51_47_PM_vBldYuc.png','https://clicky.id/arifex21','#6366f1','#4f46e5','linear','to right',0,1,'2025-07-28 13:40:29.630380','2025-08-03 09:56:45.892585');
INSERT INTO "core_service" VALUES(11,'Jasa Unduh Envato Elements Termurah','Dapatkan 10 unduhan Envato Elements hanya dengan Rp10.000!','services/ChatGPT_Image_Aug_13_2025_03_46_12_PM.png','http://lynk.id/affiliatepemula/ov177j9ewgyd/checkout','#ff05bc','#ba00c7','linear','to right',0,1,'2025-08-13 08:43:57.740194','2025-08-13 08:47:36.511223');
CREATE TABLE "core_sitesettings" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "admin_photo" varchar(100) NULL, "admin_name" varchar(100) NULL, "admin_title" varchar(100) NULL, "admin_description" text NULL, "admin_whatsapp" varchar(20) NULL, "footer_text" varchar(255) NULL, "footer_show_social" bool NOT NULL, "site_title" varchar(100) NULL, "site_description" text NULL, "site_keywords" text NULL, "site_favicon" varchar(100) NULL, "favicon_16" varchar(100) NULL, "favicon_32" varchar(100) NULL, "favicon_apple_touch" varchar(100) NULL, "favicon_android_192" varchar(100) NULL, "favicon_android_512" varchar(100) NULL, "favicon_manifest" varchar(100) NULL, "meta_author" varchar(100) NULL, "meta_robots" varchar(100) NULL, "meta_viewport" varchar(100) NULL, "og_title" varchar(100) NULL, "og_description" text NULL, "og_image" varchar(100) NULL, "twitter_card" varchar(100) NULL, "twitter_site" varchar(100) NULL);
INSERT INTO "core_sitesettings" VALUES(1,'profiles/IMG20220928081413_ZNZtIuO.jpg','Eka Syarif Maulana','Web Development','Temukan solusi kebutuhan digital & gaya hidup Anda. Mudah, cepat, dan lengkap dalam satu link','6282392115909','@BioLinkEka',0,'BioLinkEka','Solusi lengkap untuk kebutuhan digital dan gaya hidup Anda. Dapatkan template PPT profesional, koleksi barang unik, dan berbagai penawaran menarik lainnya di sini.','bio link, linktree, link bio, template ppt, template powerpoint, template presentasi, barang unik, hadiah unik, produk unik, koleksi unik, digital products, jual online, marketplace, toko online, produk kreatif, layanan digital','','','','','','','','','index, follow','width=device-width, initial-scale=1','','','','summary_large_image','');
CREATE TABLE "core_socialmedia" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "platform" varchar(30) NOT NULL, "username" varchar(100) NOT NULL, "link" varchar(200) NOT NULL, "icon" varchar(50) NOT NULL, "description" text NULL, "is_active" bool NOT NULL, "order" integer NOT NULL);
INSERT INTO "core_socialmedia" VALUES(1,'whatsapp','whatsapp','https://wa.me/6282392115909','fab fa-whatsapp','',1,1);
INSERT INTO "core_socialmedia" VALUES(2,'instagram','arif_ex21','https://www.instagram.com/arif_ex21?igsh=a3pqaTNodWFrdXVv','fab fa-instagram','',1,0);
INSERT INTO "core_socialmedia" VALUES(3,'telegram','telegram','https://t.me/arif_ex21','fab fa-telegram','',1,0);
INSERT INTO "core_socialmedia" VALUES(5,'github','dresar','https://github.com/dresar','fab fa-github','',1,0);
INSERT INTO "core_socialmedia" VALUES(6,'linkedin','arifex21','https://www.linkedin.com/in/arifex21','fab fa-linkedin','',1,0);
INSERT INTO "core_socialmedia" VALUES(7,'facebook','ekasyarifmaulana','https://web.facebook.com/profile.php?id=100051313127762','fab fa-facebook','',1,0);
INSERT INTO "core_socialmedia" VALUES(8,'tiktok','arif_ex21','https://www.tiktok.com/arif_ex21','fab fa-tiktok','',1,0);
CREATE TABLE "core_userprofile" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "display_name" varchar(100) NULL, "title" varchar(100) NULL, "photo" varchar(100) NULL, "description" text NULL, "whatsapp" varchar(20) NULL, "slug" varchar(100) NOT NULL UNIQUE, "is_active" bool NOT NULL, "created_at" datetime NULL, "updated_at" datetime NULL, "created_by_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "login_count" integer NOT NULL);
INSERT INTO "core_userprofile" VALUES(2,'eka','Web Development','profiles/IMG20220928081413_ZNZtIuO.jpg','Temukan solusi kebutuhan digital & gaya hidup Anda. Mudah, cepat, dan lengkap dalam satu link','6282392115909','eka',1,'2025-08-03 09:15:35.407281','2025-12-25 03:21:21.789256',NULL,2,4);
CREATE TABLE "core_whatsapptemplate" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL, "category" varchar(30) NOT NULL, "message" text NOT NULL, "description" varchar(200) NULL, "is_active" bool NOT NULL, "order" integer NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
INSERT INTO "core_whatsapptemplate" VALUES(30,'Pertanyaan Jasa Website','business','Halo min, saya mau tanya nih. Bisa joki website gak? Kira-kira berapa biayanya ya? Dan berapa lama pengerjaannya?','Template untuk customer yang bertanya tentang jasa pembuatan website',1,1,'2025-08-03 04:34:47.717616','2025-08-03 04:34:47.717649');
INSERT INTO "core_whatsapptemplate" VALUES(31,'Tanya Harga Aplikasi Mobile','business','Min, mau tanya dong. Kalau bikin aplikasi mobile Android/iOS kira-kira habis berapa ya? Ada paket hemat gak?','Template untuk pertanyaan harga aplikasi mobile',1,2,'2025-08-03 04:34:47.724868','2025-08-03 04:34:47.724887');
INSERT INTO "core_whatsapptemplate" VALUES(32,'Konsultasi Project','business','Halo kak, saya ada project nih. Bisa konsultasi dulu gak? Saya mau bikin {jenis_project} tapi masih bingung mulai dari mana.','Template untuk customer yang ingin konsultasi project',1,3,'2025-08-03 04:34:47.728182','2025-08-03 04:34:47.728197');
INSERT INTO "core_whatsapptemplate" VALUES(33,'Tanya Portfolio','business','Min, boleh liat portfolio website yang udah pernah dibuat gak? Saya mau liat contoh-contohnya dulu sebelum order.','Template untuk customer yang ingin melihat portfolio',1,4,'2025-08-03 04:34:47.731391','2025-08-03 04:34:47.731408');
INSERT INTO "core_whatsapptemplate" VALUES(34,'Pertanyaan Maintenance','business','Kak, kalau udah jadi websitenya, ada layanan maintenance gak? Soalnya saya gak ngerti teknis-teknisnya.','Template untuk pertanyaan tentang layanan maintenance',1,5,'2025-08-03 04:34:47.734931','2025-08-03 04:34:47.734948');
INSERT INTO "core_whatsapptemplate" VALUES(35,'Tanya Revisi','business','Min, kalau misalnya ada yang mau diubah atau revisi, bisa gak? Ada batasan revisi berapa kali?','Template untuk pertanyaan tentang revisi',1,6,'2025-08-03 04:34:47.738388','2025-08-03 04:34:47.738409');
INSERT INTO "core_whatsapptemplate" VALUES(36,'Pertanyaan Hosting Domain','business','Kak, untuk hosting sama domain gimana? Apa saya yang siapin sendiri atau dari sana yang urus?','Template untuk pertanyaan hosting dan domain',1,7,'2025-08-03 04:34:47.742405','2025-08-03 04:34:47.742424');
INSERT INTO "core_whatsapptemplate" VALUES(37,'Tanya Waktu Pengerjaan','business','Min, kalau order sekarang kira-kira kapan selesainya? Saya butuhnya agak urgent nih.','Template untuk pertanyaan waktu pengerjaan',1,8,'2025-08-03 04:34:47.745736','2025-08-03 04:34:47.745753');
INSERT INTO "core_whatsapptemplate" VALUES(38,'Pertanyaan Payment','business','Kak, untuk pembayarannya gimana? Bisa cicil gak? Atau harus lunas di depan?','Template untuk pertanyaan sistem pembayaran',1,9,'2025-08-03 04:34:47.749293','2025-08-03 04:34:47.749309');
INSERT INTO "core_whatsapptemplate" VALUES(39,'Tanya Fitur Custom','business','Min, saya mau tambah fitur {nama_fitur} di websitenya. Bisa gak ya? Kena charge tambahan berapa?','Template untuk pertanyaan fitur custom',1,10,'2025-08-03 04:34:47.753387','2025-08-03 04:34:47.753405');
INSERT INTO "core_whatsapptemplate" VALUES(40,'Salam Pembuka Customer','greeting','Halo min, selamat {waktu}! Saya mau tanya-tanya tentang jasa yang tersedia dong.','Template salam pembuka dari customer',1,11,'2025-08-03 04:34:47.757792','2025-08-03 04:34:47.757809');
INSERT INTO "core_whatsapptemplate" VALUES(41,'Pertanyaan SEO','business','Kak, websitenya nanti udah SEO friendly belum? Biar gampang muncul di Google gitu.','Template untuk pertanyaan SEO',1,12,'2025-08-03 04:34:47.761311','2025-08-03 04:34:47.761329');
INSERT INTO "core_whatsapptemplate" VALUES(42,'Tanya Responsive Design','business','Min, websitenya nanti bisa dibuka di HP juga kan? Tampilannya bagus gak di mobile?','Template untuk pertanyaan responsive design',1,13,'2025-08-03 04:34:47.765655','2025-08-03 04:34:47.765674');
INSERT INTO "core_whatsapptemplate" VALUES(43,'Pertanyaan E-commerce','business','Kak, bisa bikin toko online gak? Yang ada keranjang belanja, payment gateway, sama tracking ordernya.','Template untuk pertanyaan e-commerce',1,14,'2025-08-03 04:34:47.769760','2025-08-03 04:34:47.769780');
INSERT INTO "core_whatsapptemplate" VALUES(44,'Follow Up Order','follow_up','Min, gimana nih progress websitenya? Udah sampai mana? Bisa liat preview-nya gak?','Template untuk follow up progress order',1,15,'2025-08-03 04:34:47.773175','2025-08-03 04:34:47.773193');
CREATE TABLE "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);
CREATE TABLE "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
INSERT INTO "django_content_type" VALUES(1,'admin','logentry');
INSERT INTO "django_content_type" VALUES(2,'auth','permission');
INSERT INTO "django_content_type" VALUES(3,'auth','group');
INSERT INTO "django_content_type" VALUES(4,'auth','user');
INSERT INTO "django_content_type" VALUES(5,'contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES(6,'sessions','session');
INSERT INTO "django_content_type" VALUES(7,'core','product');
INSERT INTO "django_content_type" VALUES(8,'core','service');
INSERT INTO "django_content_type" VALUES(9,'core','sitesettings');
INSERT INTO "django_content_type" VALUES(10,'core','socialmedia');
INSERT INTO "django_content_type" VALUES(11,'core','whatsapptemplate');
INSERT INTO "django_content_type" VALUES(12,'core','userprofile');
INSERT INTO "django_content_type" VALUES(13,'core','productimage');
CREATE TABLE "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);
INSERT INTO "django_migrations" VALUES(1,'contenttypes','0001_initial','2025-07-28 13:39:34.353322');
INSERT INTO "django_migrations" VALUES(2,'auth','0001_initial','2025-07-28 13:39:34.375006');
INSERT INTO "django_migrations" VALUES(3,'admin','0001_initial','2025-07-28 13:39:34.395920');
INSERT INTO "django_migrations" VALUES(4,'admin','0002_logentry_remove_auto_add','2025-07-28 13:39:34.410528');
INSERT INTO "django_migrations" VALUES(5,'admin','0003_logentry_add_action_flag_choices','2025-07-28 13:39:34.421350');
INSERT INTO "django_migrations" VALUES(6,'contenttypes','0002_remove_content_type_name','2025-07-28 13:39:34.440606');
INSERT INTO "django_migrations" VALUES(7,'auth','0002_alter_permission_name_max_length','2025-07-28 13:39:34.456444');
INSERT INTO "django_migrations" VALUES(8,'auth','0003_alter_user_email_max_length','2025-07-28 13:39:34.471596');
INSERT INTO "django_migrations" VALUES(9,'auth','0004_alter_user_username_opts','2025-07-28 13:39:34.482180');
INSERT INTO "django_migrations" VALUES(10,'auth','0005_alter_user_last_login_null','2025-07-28 13:39:34.496810');
INSERT INTO "django_migrations" VALUES(11,'auth','0006_require_contenttypes_0002','2025-07-28 13:39:34.502565');
INSERT INTO "django_migrations" VALUES(12,'auth','0007_alter_validators_add_error_messages','2025-07-28 13:39:34.513748');
INSERT INTO "django_migrations" VALUES(13,'auth','0008_alter_user_username_max_length','2025-07-28 13:39:34.527836');
INSERT INTO "django_migrations" VALUES(14,'auth','0009_alter_user_last_name_max_length','2025-07-28 13:39:34.542171');
INSERT INTO "django_migrations" VALUES(15,'auth','0010_alter_group_name_max_length','2025-07-28 13:39:34.555543');
INSERT INTO "django_migrations" VALUES(16,'auth','0011_update_proxy_permissions','2025-07-28 13:39:34.564730');
INSERT INTO "django_migrations" VALUES(17,'auth','0012_alter_user_first_name_max_length','2025-07-28 13:39:34.579506');
INSERT INTO "django_migrations" VALUES(18,'core','0001_initial','2025-07-28 13:39:34.607847');
INSERT INTO "django_migrations" VALUES(19,'sessions','0001_initial','2025-07-28 13:39:34.620930');
INSERT INTO "django_migrations" VALUES(20,'core','0002_alter_product_options_alter_service_options_and_more','2025-08-03 02:28:15.323261');
INSERT INTO "django_migrations" VALUES(21,'core','0003_alter_product_additional_link_alter_product_link','2025-08-03 03:50:57.878979');
INSERT INTO "django_migrations" VALUES(22,'core','0004_userprofile_login_count','2025-08-03 04:39:59.928467');
CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);
INSERT INTO "django_session" VALUES('6pfa0nl9oqizenjcmc1zyzaul5s0k2c3','.eJxVjEEOwiAQRe_C2hBokQGX7j0DmWFAqgaS0q6Md7dNutDtf-_9twi4LiWsPc1hYnERWpx-N8L4THUH_MB6bzK2uswTyV2RB-3y1ji9rof7d1Cwl602FFVWOqMjQKAxWSDUZzBxoGjjAMYiKmTOVqFjw7wh8ADeq1E5LT5fAow4KA:1ugO5y:wk7vqx0l7KwIGFRXXhyG7wmb5tepWTZilzgJvePrd4g','2025-08-11 13:40:50.095398');
INSERT INTO "django_session" VALUES('pjy7kk2aj38weders09yplj4kd88iamu','.eJxVjEEOwiAQRe_C2hBokQGX7j0DmWFAqgaS0q6Md7dNutDtf-_9twi4LiWsPc1hYnERWpx-N8L4THUH_MB6bzK2uswTyV2RB-3y1ji9rof7d1Cwl602FFVWOqMjQKAxWSDUZzBxoGjjAMYiKmTOVqFjw7wh8ADeq1E5LT5fAow4KA:1ugQXX:n9cOj1Kp1tLiApM6pWJLh8oO6DwPqmyNimiN17Br1qM','2025-08-11 16:17:27.656688');
INSERT INTO "django_session" VALUES('3a44ftv83s1jwz9j9cii9gmdwa5gu0sl','.eJxVjEEOwiAQRe_C2hBokQGX7j0DmWFAqgaS0q6Md7dNutDtf-_9twi4LiWsPc1hYnERWpx-N8L4THUH_MB6bzK2uswTyV2RB-3y1ji9rof7d1Cwl602FFVWOqMjQKAxWSDUZzBxoGjjAMYiKmTOVqFjw7wh8ADeq1E5LT5fAow4KA:1ugccf:aLVe5CbXoWV8StWtWpsEzqJaiVlRGhxEZF0MwBjE3Sk','2025-08-12 05:11:33.499959');
INSERT INTO "django_session" VALUES('g7gov9tla4v5vli89rbd4r2beikovqi4','.eJxVjEEOwiAQRe_C2hBokQGX7j0DmWFAqgaS0q6Md7dNutDtf-_9twi4LiWsPc1hYnERWpx-N8L4THUH_MB6bzK2uswTyV2RB-3y1ji9rof7d1Cwl602FFVWOqMjQKAxWSDUZzBxoGjjAMYiKmTOVqFjw7wh8ADeq1E5LT5fAow4KA:1ugclY:LwSFLvWvV8MP-L9SO-wRxJkhfu_JMxp9AmJAZjJdTfo','2025-08-12 05:20:44.689105');
INSERT INTO "django_session" VALUES('eeey3wotjg1qhv985xvd6izamoemobgz','.eJxVjEEOwiAQRe_C2hBokQGX7j0DmWFAqgaS0q6Md7dNutDtf-_9twi4LiWsPc1hYnERWpx-N8L4THUH_MB6bzK2uswTyV2RB-3y1ji9rof7d1Cwl602FFVWOqMjQKAxWSDUZzBxoGjjAMYiKmTOVqFjw7wh8ADeq1E5LT5fAow4KA:1ugcqM:LJZDzqs3I2VjnshpmAxjecoWpYubYuklR1lnQUcY_Cs','2025-08-12 05:25:42.826740');
INSERT INTO "django_session" VALUES('r3nett1z89kkbasyetk6ss3kmbo8jq0i','.eJxVjEEOwiAQRe_C2hBokQGX7j0DmWFAqgaS0q6Md7dNutDtf-_9twi4LiWsPc1hYnERWpx-N8L4THUH_MB6bzK2uswTyV2RB-3y1ji9rof7d1Cwl602FFVWOqMjQKAxWSDUZzBxoGjjAMYiKmTOVqFjw7wh8ADeq1E5LT5fAow4KA:1uiB3u:MHkjTV1yRkPJpJ9FVfey1dOq1dDhEb7A0eK5Sj_x1lA','2025-08-16 12:10:06.133314');
INSERT INTO "django_session" VALUES('ns5wkn3zpqc39prgmwyyhghf49gr9qoa','.eJxVjEEOwiAQRe_C2hBokQGX7j0DmWFAqgaS0q6Md7dNutDtf-_9twi4LiWsPc1hYnERWpx-N8L4THUH_MB6bzK2uswTyV2RB-3y1ji9rof7d1Cwl602FFVWOqMjQKAxWSDUZzBxoGjjAMYiKmTOVqFjw7wh8ADeq1E5LT5fAow4KA:1uiN44:3XmpBIpmkRwbkFZx43t-ZAVyGJlvYns0ilYv40Ajjg0','2025-08-17 00:59:04.474953');
INSERT INTO "django_session" VALUES('tzuzv2bxv43oktekgtxxmkpozpqjtc35','.eJxVjDsOwjAQBe_iGlm2499S0nMGa9fe4ACypXwqxN0hUgpo38y8l0i4rTVtC89pKuIstDj9boT5wW0H5Y7t1mXubZ0nkrsiD7rIay_8vBzu30HFpX5rMzgH4J0lP-YSwBeOGtgxW214HAzGMGRlo4fMTrFGIogUjCWlAIt4fwDSaje3:1uiNdK:hphwbSksuxOV4PwQqpLt57qTbcBjeRpgWyYVLVWojiA','2025-08-17 01:35:30.973616');
INSERT INTO "django_session" VALUES('duzrnub5ofwiyo1d0v65qhfkoqcjzkea','.eJxVjDsOwjAQBe_iGlm2499S0nMGa9fe4ACypXwqxN0hUgpo38y8l0i4rTVtC89pKuIstDj9boT5wW0H5Y7t1mXubZ0nkrsiD7rIay_8vBzu30HFpX5rMzgH4J0lP-YSwBeOGtgxW214HAzGMGRlo4fMTrFGIogUjCWlAIt4fwDSaje3:1uiNiU:JMFaUnK9zZk20uKZzvncJWPchlkLmzeWeTsk0RN0UYs','2025-08-17 01:40:50.681251');
INSERT INTO "django_session" VALUES('db468mal9cc5b38p6rq4xsjiwmkddge4','.eJxVjDsOwjAQBe_iGlm2499S0nMGa9fe4ACypXwqxN0hUgpo38y8l0i4rTVtC89pKuIstDj9boT5wW0H5Y7t1mXubZ0nkrsiD7rIay_8vBzu30HFpX5rMzgH4J0lP-YSwBeOGtgxW214HAzGMGRlo4fMTrFGIogUjCWlAIt4fwDSaje3:1uiPF2:OuCuL7Epmj1alhcTf_Sjo34htU0n1yzWuhtObrIMIYg','2025-08-17 03:18:32.576057');
INSERT INTO "django_session" VALUES('lxx2fo6o4166fettdkvupdck2ptzk8ap','.eJxVjMsOwiAUBf-FtSEFwsule7-B3AdI1UBS2pXx37VJF7o9M3NeIsG21rSNvKSZxVkocfrdEOiR2w74Du3WJfW2LjPKXZEHHfLaOT8vh_t3UGHUb-3IomMVJy7GavQUDGP0ZB0UtJomdkBA3mVfNAMgZxNUYAwYS7FFvD8KVTmL:1uiUYd:8mtqfHU0oOQghinXsK_x_hD9I6SfWzdd3tFXzGHcjjs','2025-08-17 08:59:07.937594');
INSERT INTO "django_session" VALUES('kaorqercte8oradzsr77g9h61bburvpn','.eJxVjDsOwjAQBe_iGlnrP6akzxms9XqDA8iR4qRC3B0ipYD2zcx7iYTbWtPWeUlTERehxel3y0gPbjsod2y3WdLc1mXKclfkQbsc5sLP6-H-HVTs9VvDmdCP5MkDmtHZ4BVoDFgMsy7o2AXlTIDIFHXWrCwDkI0UgyGgKN4f5uU3xg:1uiUoa:qXbq4eUTGTEC_3blsMXu7eK-6olN3V16B6PQDthC96s','2025-08-17 09:15:36.079461');
INSERT INTO "django_session" VALUES('hxivcuuhftjwpqy8vhfv2g3onpb2sqqu','.eJxVjDsOwjAQBe_iGlnrP6akzxms9XqDA8iR4qRC3B0ipYD2zcx7iYTbWtPWeUlTERehxel3y0gPbjsod2y3WdLc1mXKclfkQbsc5sLP6-H-HVTs9VvDmdCP5MkDmtHZ4BVoDFgMsy7o2AXlTIDIFHXWrCwDkI0UgyGgKN4f5uU3xg:1uiUrI:Dl11OLM4q4gtCdciyvKzlVDgAxbkPTn8C3smaEWImCk','2025-08-17 09:18:24.782105');
INSERT INTO "django_session" VALUES('r71yggafmy5niy759u8et4jqrefj9jc3','.eJxVjDsOwjAQBe_iGlnrP6akzxms9XqDA8iR4qRC3B0ipYD2zcx7iYTbWtPWeUlTERehxel3y0gPbjsod2y3WdLc1mXKclfkQbsc5sLP6-H-HVTs9VvDmdCP5MkDmtHZ4BVoDFgMsy7o2AXlTIDIFHXWrCwDkI0UgyGgKN4f5uU3xg:1uim0A:GN3ZmKQ6uZ99uPi58UQExMUmaikw1-svUwmURy-cOG8','2025-08-18 03:36:42.471216');
INSERT INTO "django_session" VALUES('7e66zvzl6izedlawajfhdpjluwp2gjvw','.eJxVjDsOwjAQBe_iGlnrP6akzxms9XqDA8iR4qRC3B0ipYD2zcx7iYTbWtPWeUlTERehxel3y0gPbjsod2y3WdLc1mXKclfkQbsc5sLP6-H-HVTs9VvDmdCP5MkDmtHZ4BVoDFgMsy7o2AXlTIDIFHXWrCwDkI0UgyGgKN4f5uU3xg:1vYbuk:xbPvkkS2dNO7Bspsio9qPorKUF2kKejPprDZkvIsOU8','2026-01-08 03:21:22.423847');
CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");
CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");
CREATE UNIQUE INDEX "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" ("user_id", "group_id");
CREATE INDEX "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" ("user_id");
CREATE INDEX "auth_user_groups_group_id_97559544" ON "auth_user_groups" ("group_id");
CREATE UNIQUE INDEX "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" ("user_id", "permission_id");
CREATE INDEX "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" ("user_id");
CREATE INDEX "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" ("permission_id");
CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");
CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");
CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");
CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");
CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");
CREATE INDEX "core_productimage_product_id_10178291" ON "core_productimage" ("product_id");
CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");
CREATE INDEX "core_userprofile_created_by_id_fd2ec7f1" ON "core_userprofile" ("created_by_id");
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('django_migrations',22);
INSERT INTO "sqlite_sequence" VALUES('django_admin_log',0);
INSERT INTO "sqlite_sequence" VALUES('django_content_type',13);
INSERT INTO "sqlite_sequence" VALUES('auth_permission',52);
INSERT INTO "sqlite_sequence" VALUES('auth_group',0);
INSERT INTO "sqlite_sequence" VALUES('auth_user',2);
INSERT INTO "sqlite_sequence" VALUES('core_sitesettings',1);
INSERT INTO "sqlite_sequence" VALUES('core_socialmedia',8);
INSERT INTO "sqlite_sequence" VALUES('core_service',11);
INSERT INTO "sqlite_sequence" VALUES('core_whatsapptemplate',44);
INSERT INTO "sqlite_sequence" VALUES('core_product',43);
INSERT INTO "sqlite_sequence" VALUES('core_productimage',51);
INSERT INTO "sqlite_sequence" VALUES('core_userprofile',2);
COMMIT;
