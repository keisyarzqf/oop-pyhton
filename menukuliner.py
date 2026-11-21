class TemanKuliner:

    MENU_TERSEDIA = {
        "kopi susu gula aren": 18000,
        "matcha latte": 22000,
        "dimsum mentai": 25000,
        "cheesecake tiramisu": 28000,
    }

    def __init__(self, nama_asisten: str, nama_pelanggan: str, saldo: int = 0):
        if not isinstance(nama_asisten, str) or not nama_asisten.strip():
            raise ValueError("Nama asisten harus berupa teks dan tidak boleh kosong.")
        if not isinstance(nama_pelanggan, str) or not nama_pelanggan.strip():
            raise ValueError("Nama pelanggan harus berupa teks dan tidak boleh kosong.")
        if not isinstance(saldo, (int, float)) or isinstance(saldo, bool) or saldo < 0:
            raise ValueError("Saldo tidak boleh bernilai negatif.")

        self.nama_asisten = nama_asisten.strip().title()
        self.nama_pelanggan = nama_pelanggan.strip().title()
        self.saldo = int(saldo)
        self.keranjang: list[str] = []

    def perkenalan(self) -> str:
        daftar_menu = ", ".join(
            f"{menu.title()} (Rp{harga:,})".replace(",", ".")
            for menu, harga in self.MENU_TERSEDIA.items()
        )
        saldo_format = f"Rp{self.saldo:,}".replace(",", ".")
        return (
            f"Halo {self.nama_pelanggan}! Saya {self.nama_asisten}, asisten kedai kamu hari ini.\n"
            f"Saldo kamu saat ini: {saldo_format}.\n"
            f"Menu yang tersedia: {daftar_menu}."
        )

    def tambah_pesanan(self, nama_menu: str) -> str:
        """Method tambahan untuk menambahkan item menu ke keranjang."""
        key = nama_menu.strip().lower()
        if key not in self.MENU_TERSEDIA:
            return f"Maaf {self.nama_pelanggan}, menu '{nama_menu}' belum tersedia di kedai."

        harga = self.MENU_TERSEDIA[key]
        if self.saldo < harga:
            kurang = f"Rp{harga - self.saldo:,}".replace(",", ".")
            return (
                f"Saldo kamu belum cukup untuk {key.title()}. "
                f"Masih kurang {kurang}."
            )

        self.saldo -= harga
        self.keranjang.append(key.title())
        sisa_saldo = f"Rp{self.saldo:,}".replace(",", ".")
        return (
            f"Sip! {key.title()} berhasil ditambahkan ke pesanan kamu. "
            f"Sisa saldo: {sisa_saldo}."
        )

    def respons(self, pesan: str) -> str:
        """Method utama untuk merespons input atau perintah dari pelanggan."""
        if not isinstance(pesan, str) or not pesan.strip():
            return f"Silakan ketik pesan atau nama menu, {self.nama_pelanggan}."

        teks = pesan.strip().lower()

        if "halo" in teks or "hai" in teks or "siapa" in teks:
            return f"Hai {self.nama_pelanggan}! Ada yang bisa {self.nama_asisten} bantu hari ini?"

        if "menu" in teks:
            return self.perkenalan()

        if "keranjang" in teks or "pesanan" in teks:
            if not self.keranjang:
                return f"Keranjang kamu masih kosong, {self.nama_pelanggan}."
            return f"Pesanan kamu saat ini: {', '.join(self.keranjang)}."

        if "saldo" in teks:
            saldo_format = f"Rp{self.saldo:,}".replace(",", ".")
            return f"Sisa saldo kamu sekarang {saldo_format}, {self.nama_pelanggan}."

        for menu in self.MENU_TERSEDIA:
            if menu in teks:
                return self.tambah_pesanan(menu)

        return (
            f"Maaf {self.nama_pelanggan}, {self.nama_asisten} belum memahami maksud "
            f"'{pesan.strip()}'. Coba tanya 'menu', 'saldo', atau sebut nama menu."
        )


def buat_sesi_pelanggan() -> TemanKuliner:
    
    while True:
        nama_pelanggan = input("Masukkan nama pelanggan: ")
        nama_asisten = input("Masukkan nama asisten (Enter = 'Bibol'): ").strip() or "Bibol"
        saldo_mentah = input("Masukkan saldo awal (angka): ").strip()

        try:
            saldo = int(saldo_mentah)
            return TemanKuliner(
                nama_asisten=nama_asisten,
                nama_pelanggan=nama_pelanggan,
                saldo=saldo,
            )
        except ValueError as err:
            print(f"[Error] {err} Silakan ulangi input data.\n")


def jalankan_sesi_chat(sesi: TemanKuliner) -> None:
    print("\n" + sesi.perkenalan())
    print("(Ketik 'selesai' untuk kembali ke menu utama simulator)\n")

    while True:
        pesan = input(f"{sesi.nama_pelanggan}: ")
        if pesan.strip().lower() == "selesai":
            print(f"{sesi.nama_asisten}: Terima kasih sudah mampir, {sesi.nama_pelanggan}!\n")
            break
        print(f"{sesi.nama_asisten}: {sesi.respons(pesan)}")


def jalankan_simulator() -> None:
    riwayat_sesi: list[TemanKuliner] = []

    print("=== SIMULATOR KEDAI TEMANKULINER ===")
    while True:
        print("1. Input data pelanggan baru & mulai chat")
        print("2. Lihat rekap sesi pelanggan yang sudah masuk")
        print("3. Keluar")
        pilihan = input("Pilih menu (1/2/3): ").strip()

        if pilihan == "1":
            print()
            sesi = buat_sesi_pelanggan()
            riwayat_sesi.append(sesi)
            jalankan_sesi_chat(sesi)

        elif pilihan == "2":
            print("\n--- Rekap Sesi Pelanggan ---")
            if not riwayat_sesi:
                print("Belum ada data pelanggan yang diinput.")
            else:
                for idx, item in enumerate(riwayat_sesi, start=1):
                    saldo_fmt = f"Rp{item.saldo:,}".replace(",", ".")
                    pesanan_str = ", ".join(item.keranjang) if item.keranjang else "Belum ada"
                    print(
                        f"{idx}. Pelanggan: {item.nama_pelanggan} | "
                        f"Asisten: {item.nama_asisten} | "
                        f"Saldo: {saldo_fmt} | "
                        f"Pesanan: {pesanan_str}"
                    )
            print()

        elif pilihan == "3":
            print("Simulator ditutup. Sampai jumpa!")
            break

        else:
            print("Pilihan tidak valid. Masukkan 1, 2, atau 3.\n")


if __name__ == "__main__":
    jalankan_simulator()