from downloader import unduh_jurnal_pdf
from questionary import confirm
from ui import show_banner, get_user_input, loading_dummy
from rich.console import Console
from search import cari_jurnal

console = Console()

def main():
    show_banner()
    data = get_user_input()
    loading_dummy("menghubungkan ke sumber jurnal terpercaya...")

    console.print("\n[bold green]Data pencarian kamu:[/bold green]")
    console.print(f"Judul      : {data['judul']}")
    console.print(f"Jurusan    : {data['jurusan']}")
    console.print(f"Jenis      : {data['jenis']}")
    console.print(f"Tahun      : {data['tahun_awal']} - {data['tahun_akhir']}")
    console.print(f"Jumlah     : {data['jumlah']}")
    console.print(f"Format     : {data['format_file'].upper()}")

    hasil_jurnal = cari_jurnal(data)

    if not hasil_jurnal:
        console.print("[bold red]❌ Tidak ditemukan hasil jurnal sesuai kriteria.[/bold red]")
        return

    if confirm("Apakah kamu ingin langsung mengunduh jurnal-jurnal ini?").ask():
        unduh_jurnal_pdf(hasil_jurnal, data["format_file"])
    else:
        console.print("[yellow]❗ unduhan dibatalkan. link jurnal sudah ditampilkan di atas.[/yellow]")

if __name__ == "__main__":
    main()
