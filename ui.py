from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from datetime import datetime
import questionary
import time

console = Console()

def show_banner():
    console.print(Panel.fit(
        "[bold cyan]JURNAL FINDER v1.0[/bold cyan]\n"
        "[green]search jurnal nasional/internasional[/green]\n"
        f"[yellow]Waktu: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}[/yellow]\n"
        "[magenta]Author: beruu27[/magenta]",
        title=":satellite: JurnalFinder", border_style="blue"
    ))

def get_user_input():
    jurusan = questionary.text("bidang Studi (misal: akuntansi, manajemen, dll):").ask()
    judul = questionary.text("masukkan judul jurnal yang dicari:").ask()
    jenis = questionary.select("pilih jenis jurnal:", choices=["Nasional (SINTA ≥ 3)", "Internasional"]).ask()
    tahun_awal = questionary.text("masukkan tahun awal (contoh: 2020):").ask()
    tahun_akhir = questionary.text("masukkan tahun akhir (contoh: 2024):").ask()
    jumlah = questionary.text("berapa jumlah jurnal yang ingin dicari?").ask()
    format_file = questionary.select("pilih format file yang ingin disimpan:", choices=["PDF", "Word"]).ask()

    return {
        "jurusan": jurusan,
        "judul": judul,
        "jenis": jenis,
        "tahun_awal": int(tahun_awal),
        "tahun_akhir": int(tahun_akhir),
        "jumlah": int(jumlah),
        "format_file": format_file.lower()
    }

def loading_dummy(task_msg="Mencari jurnal..."):
    with Progress() as progress:
        task = progress.add_task(f"[cyan]{task_msg}", total=100)
        while not progress.finished:
            progress.update(task, advance=10)
            time.sleep(0.2)

def main():
    show_banner()
    data = get_user_input()
    loading_dummy("Menghubungkan ke sumber jurnal terpercaya...")

    console.print("\n[bold green]Data pencarian kamu:[/bold green]")
    console.print(f"Judul      : {data['judul']}")
    console.print(f"Jurusan    : {data['jurusan']}")
    console.print(f"Jenis      : {data['jenis']}")
    console.print(f"Tahun      : {data['tahun_awal']} - {data['tahun_akhir']}")
    console.print(f"Jumlah     : {data['jumlah']}")
    console.print(f"Format     : {data['format_file'].upper()}")
    
    console.print("\n[bold yellow]Fitur pencarian real (SINTA/Google Scholar/DOAJ) akan ditambahkan di tahap berikutnya...[/bold yellow]")

if __name__ == "__main__":
    main()
