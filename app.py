from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder='src/templates', static_folder='src/static')


@app.route("/", methods=["GET", "POST"])
def home():
    # Load the list of composers
    api_url = "https://api.openopus.org/work/dump.json"  # Change this if you find a broader endpoint
COMPOSERS = [
    "John Adams", "Thomas Adès", "Isaac Albéniz", "Tomaso Albinoni", "George Antheil",
    "Malcolm Arnold", "Milton Babbitt", "Johann Sebastian Bach", "Carl Philipp Emanuel Bach",
    "Johann Christian Bach", "Mily Balakirev", "Samuel Barber", "Béla Bartók", "Arnold Bax",
    "Ludwig van Beethoven", "Vincenzo Bellini", "Alban Berg", "Luciano Berio", "Hector Berlioz",
    "Leonard Bernstein", "Franz Berwald", "Heinrich Franz von Biber", "Harrison Birtwistle",
    "Georges Bizet", "Ernest Bloch", "Luigi Boccherini", "Alexander Borodin", "Pierre Boulez",
    "Joly Braga Santos", "Johannes Brahms", "Benjamin Britten", "Max Bruch", "Anton Bruckner",
    "Ferruccio Busoni", "Dietrich Buxtehude", "William Byrd", "John Cage", "Camargo Guarnieri",
    "Elliott Carter", "Emmanuel Chabrier", "Marc-Antoine Charpentier", "Ernest Chausson",
    "Carlos Chávez", "Luigi Cherubini", "Frédéric Chopin", "Aaron Copland", "Arcangelo Corelli",
    "John Corigliano", "François Couperin", "George Crumb", "César Cui", "Vincent d'Indy",
    "Michael Daugherty", "Claude Debussy", "Léo Delibes", "Frederick Delius", "Josquin Des Prez",
    "Karl Ditters von Dittersdorf", "Ernst von Dohnányi", "Gaetano Donizetti", "John Dowland",
    "Guillaume Dufay", "Paul Dukas", "Maurice Duruflé", "Henri Dutilleux", "Antonín Dvořák",
    "Edward Elgar", "George Enescu", "Manuel de Falla", "Gabriel Fauré", "John Field",
    "César Franck", "Girolamo Frescobaldi", "George Gershwin", "Carlo Gesualdo", "Orlando Gibbons",
    "Alberto Ginastera", "Philip Glass", "Alexander Glazunov", "Reinhold Glière",
    "Mikhail Ivanovich Glinka", "Christoph Willibald von Gluck", "Karl Goldmark",
    "Antonio Carlos Gomes", "Henryk Górecki", "Morton Gould", "Charles Gounod", "Percy Grainger",
    "Enrique Granados", "Edvard Grieg", "Sofia Gubaidulina", "George Frideric Handel",
    "Howard Hanson", "Roy Harris", "Franz Joseph Haydn", "Hans Werner Henze", "Victor Herbert",
    "Paul Hindemith", "Vagn Holmboe", "Gustav Holst", "Arthur Honegger", "Johann Nepomuk Hummel",
    "Engelbert Humperdinck", "Jacques Ibert", "Charles Ives", "Leoš Janáček", "Clément Janequin",
    "Scott Joplin", "Dmitry Kabalevsky", "Aram Khachaturian", "Zoltán Kodály",
    "Erich Wolfgang Korngold", "Edouard Lalo", "Orlande de Lassus", "Ruggero Leoncavallo",
    "Léonin", "György Ligeti", "Franz Liszt", "Fernando Lopes-Graça", "Jean-Baptiste Lully",
    "Witold Lutoslawski", "Edward MacDowell", "Guillaume de Machaut", "Gustav Mahler",
    "Marin Marais", "Benedetto Marcello", "Alessandro Marcello", "Bohuslav Martinů",
    "Pietro Mascagni", "Jules Massenet", "Felix Mendelssohn", "Olivier Messiaen",
    "Francisco Mignone", "Darius Milhaud", "Ernest Moeran", "Claudio Monteverdi",
    "Wolfgang Amadeus Mozart", "Modest Mussorgsky", "Carl Nielsen", "Luigi Nono", "Jacob Obrecht",
    "Johannes Ockeghem", "Jacques Offenbach", "Carl Orff", "Johann Pachelbel", "Niccolò Paganini",
    "Giovanni Pierluigi da Palestrina", "Arvo Pärt", "Krzysztof Penderecki",
    "Giovanni Battista Pergolesi", "Pérotin", "Astor Piazzolla", "Francis Poulenc",
    "Michael Praetorius", "Sergei Prokofiev", "Giacomo Puccini", "Henry Purcell",
    "Sergei Rachmaninoff", "Jean-Philippe Rameau", "Einojuhani Rautavaara", "Maurice Ravel",
    "Max Reger", "Steve Reich", "Ottorino Respighi", "Wolfgang Rihm", "Nikolai Rimsky-Korsakov",
    "Joaquín Rodrigo", "Ned Rorem", "Gioachino Rossini", "Albert Roussel", "Camille Saint-Saëns",
    "Antonio Salieri", "Erik Satie", "Domenico Scarlatti", "Alessandro Scarlatti",
    "Franz Schmidt", "Alfred Schnittke", "Arnold Schoenberg", "Franz Schubert",
    "William Schuman", "Robert Schumann", "Heinrich Schütz", "Alexander Scriabin",
    "Dmitri Shostakovich", "Jean Sibelius", "Bedrich Smetana", "Fernando Sor", "Louis Spohr",
    "Carl Stamitz", "Wilhelm Stenhammar", "Karlheinz Stockhausen", "Richard Strauss",
    "Johann Strauss Jr", "Igor Stravinsky", "Josef Suk", "Jan Pieterszoon Sweelinck",
    "Karol Szymanowski", "Toru Takemitsu", "Thomas Tallis", "Giuseppe Tartini", "John Taverner",
    "Pyotr Ilyich Tchaikovsky", "Georg Philipp Telemann", "Michael Tippett", "Edgard Varèse",
    "Ralph Vaughan Williams", "Giuseppe Verdi", "Tomás Luis de Victoria", "Heitor Villa-Lobos",
    "Antonio Vivaldi", "Richard Wagner", "William Walton", "Carl Maria von Weber", "Anton Webern",
    "Kurt Weill", "Charles-Marie Widor", "Hugo Wolf", "Iannis Xenakis", "Eugene Ysaÿe",
    "Alexander von Zemlinsky"
]

@app.route("/")
def hello_world():
    return render_template("about.html", composers=COMPOSERS)

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/library")
def library():
    return render_template("library.html")

@app.route("/search", methods=["POST"])
def search_composers():
    selected_composer = request.form.get("composer_name")

    api_url = f"https://api.openopus.org/composer/list/search/{selected_composer}.json"
    response = requests.get(api_url)

    composers = []
    if response.status_code == 200:
        data = response.json()
        composers = data.get("composers", [])
    else:
        return f"Failed to fetch composers. Status Code: {response.status_code}"

    # Render the form with the list of composers
    return render_template("form.html", composers=composers)


@app.route("/search", methods=["POST"])
def search():
    # Get user input from the form
    user_name = request.form.get("name")
    selected_composer_id = request.form.get("composer_name")  # Using ID or slug from dropdown

    # Fetch the works of the selected composer using their ID/slug
    works_url = f"https://api.openopus.org/work/dump/composer/{selected_composer_id}.json"
    response = requests.get(works_url)

    works = []
    if response.status_code == 200:
        data = response.json()
        works = data.get("works", [])
    else:
        return f"Failed to fetch works for composer ID {selected_composer_id}. Status Code: {response.status_code}"

    # Render the results page
    return render_template(
        "results.html",
        name=user_name,
        selected_composer=selected_composer_id,
        works=works
    )


@app.route("/library")
def library():
    return render_template("library.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
