import requests
from rich.console import Console

console = Console()

def cari_jurnal(data):
    if data["jenis"].lower() == "nasional (sinta ≥ 3)":
        return cari_jurnal_nasional(data)
    elif data["jenis"].lower() == "internasional":
        return cari_jurnal_internasional(data)
    else:
        console.print("[red]❌ Jenis jurnal tidak dikenali![/red]")
        return []

def cari_jurnal_nasional(data):
    console.print("\n[bold green]📚 Mencari jurnal nasional (GARUDA)...[/bold green]")
    try:
        query = f"{data['judul']} {data['jurusan']}"
        url = f"https://garuda.kemdikbud.go.id/search.json?query={query}"
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            console.print(f"[red]❌ Gagal akses GARUDA: {r.status_code}[/red]")
            return []

        hasil = []
        items = r.json().get("data", [])
        for i, item in enumerate(items, 1):
            tahun = item.get("year", "-")
            if tahun != "-" and data["tahun_awal"] <= int(tahun) <= data["tahun_akhir"]:
                hasil.append({
                    "no": i,
                    "judul": item.get("title", "Tanpa Judul"),
                    "penulis": item.get("authors", "-"),
                    "tahun": tahun,
                    "link": item.get("url", "-"),
                    "doi": item.get("doi", "")
                })
            if len(hasil) >= data["jumlah"]:
                break
        return hasil
    except Exception as e:
        console.print(f"[red]❌ Gagal mencari jurnal nasional: {e}[/red]")
        return []

def cari_jurnal_internasional(data):
    hasil = []
    hasil += cari_dari_semantic_scholar(data)
    hasil += cari_dari_crossref(data)
    return hasil[:data["jumlah"]]

def cari_dari_semantic_scholar(data):
    console.print("[green]🔎 Semantic Scholar...[/green]")
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    query = f"{data['judul']} {data['jurusan']}"
    params = {
        "query": query,
        "limit": data["jumlah"],
        "fields": "title,authors,url,year"
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        hasil = []
        if r.status_code == 200:
            papers = r.json().get("data", [])
            for i, paper in enumerate(papers, 1):
                tahun = paper.get("year", "-")
                if tahun != "-" and data["tahun_awal"] <= int(tahun) <= data["tahun_akhir"]:
                    penulis = ", ".join([a.get("name", "") for a in paper.get("authors", [])])
                    hasil.append({
                        "no": i,
                        "judul": paper.get("title", "Tanpa Judul"),
                        "link": paper.get("url", "-"),
                        "penulis": penulis,
                        "tahun": tahun,
                        "doi": ""
                    })
        return hasil
    except Exception as e:
        console.print(f"[red]❌ Semantic Scholar error: {e}[/red]")
        return []

def cari_dari_crossref(data):
    console.print("[green]🌐 Crossref...[/green]")
    url = "https://api.crossref.org/works"
    query = f"{data['judul']} {data['jurusan']}"
    params = {
        "query": query,
        "rows": data["jumlah"]
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        hasil = []
        if r.status_code == 200:
            items = r.json()["message"]["items"]
            for i, item in enumerate(items, 1):
                link = item.get("URL", "-")
                tahun = item.get("published-print", {}).get("date-parts", [[None]])[0][0]
                if tahun is None:
                    tahun = item.get("published-online", {}).get("date-parts", [[None]])[0][0]
                if tahun and data["tahun_awal"] <= int(tahun) <= data["tahun_akhir"]:
                    hasil.append({
                        "no": i,
                        "judul": item.get("title", ["Tanpa Judul"])[0],
                        "link": link,
                        "penulis": ", ".join([a.get("family", "") for a in item.get("author", [])]) if "author" in item else "-",
                        "tahun": tahun,
                        "doi": item.get("DOI", "")
                    })
        return hasil
    except Exception as e:
        console.print(f"[red]❌ Crossref error: {e}[/red]")
        return []
