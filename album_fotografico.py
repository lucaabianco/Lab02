def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    try:
        infile = open(file_path, "r")
        infile.readline()
        album = dict()
        for line in infile:
            elementi = line.split(",")
            dati = []
            for x in elementi:
                dati.append(x.strip())
            if len(dati) == 5:
                codice, titolo, autore, mese, anno = dati
                mese = int(mese)
                anno = int(anno)
                if anno not in album:
                    album[anno] = [[codice, titolo, autore, mese]]
                else:
                    album[anno].append([codice, titolo, autore, mese])
        infile.close()
        return album
    except FileNotFoundError:
        return None

def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    if mese < 1 or mese > 12:
        return None
    if cerca_foto(album, codice) is not None:
        return None
    foto = [codice, titolo, autore, mese]
    try:
        test_file = open(file_path, "r")
        test_file.close()
        outfile = open(file_path, "a")
        riga = codice + "," + titolo + "," + autore + "," + str(mese) + "," + str(anno) + "\n"
        outfile.write(riga)
        outfile.close()
    except FileNotFoundError:
        return None

    if anno not in album:
        album[anno] = []
    album[anno].append(foto)

    return foto

def cerca_foto(album_aggiornato, codice):
    """Cerca una foto nell'album dato il codice"""
    for anno, foto_annuali in album_aggiornato.items():
        for foto in foto_annuali:
            if foto[0] == codice:
                return f"{foto[0]}, {foto[1]}, {foto[2]}, {foto[3]}, {anno}"

    return None

def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    if anno not in album:
        return None
    titoli = []
    for foto in album[anno]:
        titoli.append(foto[1])
    titoli.sort()
    return titoli

def main():
    album = None
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
