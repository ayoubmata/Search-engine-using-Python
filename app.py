from flask import Flask,render_template,request
import MySQLdb
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWD = "root"
DB_DATABASE = "corpus"


def index_documents(documents):
    connection = MySQLdb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD, database=DB_DATABASE)
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS documents (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), path VARCHAR(255))")


    for document in documents:
        cursor.execute("INSERT INTO documents (name, path,title,description,pathtopdf) VALUES (%s, %s, %s, %s, %s)", (document["name"], document["path"], document["title"], document["description"], document["pathtopdf"]))

    # Création de la table `keywords` si elle n'existe pas encore

    cursor.execute("CREATE TABLE IF NOT EXISTS keywords (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), documents VARCHAR(255))")

    # Indexation des documents

    for document in documents:
        # Lecture du contenu du document
        with open(document["path"], "r") as f:
            content = f.read()

        # Lemmatisation du contenu
        lemmatized_content = WordNetLemmatizer().lemmatize(content)

        # Suppression des mots vides
        stop_words = stopwords.words("french")
        mots_vides=["tous","tout","toute","toutefois","toutes","treize","trente","tres","trois","troisième","troisièmement","trop","très","tsoin","tsouin","tu","té","u","un","une","unes","uniformement","unique","uniques","uns","v","va","vais","valeur","vas","vers","via","vif","vifs","vingt","vivat","vive","vives","vlan","voici","voie","voient","voilà","voire","vont","vos","votre","vous","vous-mêmes","vu","vé","vôtre","vôtres","w","x","y","z","zut","à","â","tenant","tend","tenir","tente","tes","tic","tien","tienne","tiennes","tiens","toc","toi","toi-même","ton","touchant","toujours","ont","onze","onzième","ore","ou","ouf","ouias","oust","ouste","outre","ouvert","ouverte","ouverts","o","où","p","paf","pan","par","parce","parfois","parle","parlent","parler","parmi","parole","parseme","partant","particulier","particulière","particulièrement","pas","passé","pendant","pense","permet","personne","personnes","peu","peut","peuvent","peux","pff","pfft","pfut","pif","pire","pièce","plein","plouf","plupart","plus","plusieurs","plutôt","possessif","possessifs","possible","possibles","pouah","pour","pourquoi","pourrais","pourrait","pouvait","prealable","precisement","premier","première","premièrement","pres","probable","probante","procedant","proche","près","psitt","pu","puis","puisque","pur","pure","q","qu","quand","quant","quant-à-soi","quanta","quarante","quatorze","quatre","quatre-vingt","quatrième","quatrièmement","que","quel","quelconque","quelle","quelles","quelqu'un","quelque","quelques","quels","qui","quiconque","quinze","quoi","quoique","r","rare","rarement","rares","relative","relativement","remarquable","rend","rendre","restant","reste","restent","restrictif","retour","revoici","revoilà","rien","s","sa","sacrebleu","sait","sans","sapristi","sauf","se","sein","seize","selon","semblable","semblaient","semble","semblent","sent","sept","septième","sera","serai","seraient","serais","serait","seras","serez","seriez","serions","serons","seront","ses","seul","seule","seulement","si","sien","sienne","siennes","siens","sinon","six","sixième","soi","soi-même","soient","sois","soit","soixante","sommes","son","sont","sous","souvent","soyez","soyons","specifique","specifiques","speculatif","stop","strictement","subtiles","suffisant","suffisante","suffit","suis","suit","suivant","suivante","suivantes","suivants","suivre","sujet","superpose","sur","surtout","t","ta","tac","tandis","tant","tardive","te","tel","telle","tellement","telles","tels","dits","divers","diverse","diverses","dix","dix-huit","dix-neuf","dix-sept","dixième","doit","doivent","donc","dont","dos","douze","douzième","dring","droite","du","duquel","durant","dès","début","désormais","e","effet","egale","egalement","egales","eh","elle","elle-même","elles","elles-mêmes","en","encore","enfin","entre","envers","environ","es","essai","est","et","etant","etc","etre","eu","eue","eues","euh","eurent","eus","eusse","eussent","eusses","eussiez","eussions","eut","eux","eux-mêmes","exactement","excepté","extenso","exterieur","eûmes","eût","eûtes","f","fais","faisaient","faisant","fait","faites","façon","feront","fi","flac","floc","fois","font","force","furent","fus","fusse","fussent","fusses","fussiez","fussions","fut","fûmes","fût","fûtes","g","gens","h","ha","haut","hein","hem","hep","hi","ho","holà","hop","hormis","hors","hou","houp","hue","hui","huit","huitième","hum","hurrah","hé","hélas","i","ici","il","ils","importe","j","je","jusqu","jusque","juste","k","l","la","laisser","laquelle","las","le","lequel","les","lesquelles","lesquels","leur","leurs","longtemps","lors","lorsque","lui","lui-meme","lui-même","là","lès","m","ma","maint","maintenant","mais","malgre","malgré","maximale","me","meme","memes","merci","mes","mien","mienne","miennes","miens","mille","mince","mine","minimale","moi","moi-meme","moi-même","moindres","moins","mon","mot","moyennant","multiple","multiples","même","mêmes","n","na","naturel","naturelle","naturelles","ne","neanmoins","necessaire","necessairement","neuf","neuvième","ni","nombreuses","nombreux","nommés","non","nos","notamment","notre","nous","nous-mêmes","nouveau","nouveaux","nul","néanmoins","nôtre","nôtres","o","oh","ohé","olé","olé","on","abord", "absolument", "afin", "ah", "ai", "aie", "aient", "aies", "ailleurs", "ainsi", "ait", "allaient", "allo", "allons", "allô", "alors", "anterieur", "anterieure", "anterieures", "apres", "après", "as", "assez", "attendu", "au", "aucun", "aucune", "aucuns", "aujourd", "aujourd'hui", "aupres", "auquel", "aura", "aurai", "auraient", "aurais", "aurait", "auras", "aurez", "auriez", "aurions", "aurons", "auront", "aussi", "autant", "autre", "autrefois", "autrement", "autres", "autrui", "aux", "auxquelles", "auxquels", "avaient", "avais", "avait", "avant", "avec", "avez", "aviez", "avions", "avoir", "avons", "ayant", "ayez", "ayons", "b", "bah", "bas", "basee", "bat", "beau", "beaucoup", "bien", "bigre", "bon", "boum", "bravo", "brrr", "c", "car", "ce", "ceci", "cela", "celle", "celle-ci", "celle-là", "celles", "celles-ci", "celles-là", "celui", "celui-ci", "celui-là", "celà", "cent", "cependant", "certain", "certaine", "certaines", "certains", "certes", "ces", "cet", "cette", "ceux", "ceux-ci", "ceux-là", "chacun", "chacune", "chaque", "cher", "chers", "chez", "chiche", "chut", "chère", "chères", "ci", "cinq", "cinquantaine", "cinquante", "cinquantième", "cinquième", "clac", "clic", "combien", "comme", "comment", "comparable", "comparables", "compris", "concernant", "contre", "couic", "crac", "d", "da", "dans", "de", "debout", "dedans", "dehors", "deja", "delà", "depuis", "dernier", "derniere", "derriere", "derrière", "des", "desormais", "desquelles", "desquels", "dessous", "dessus", "deux", "deuxième", "deuxièmement", "devant", "devers", "devra", "devrait", "different", "differentes", "differents", "différent", "différente", "différentes", "différents", "dire", "directe", "directement", "dit", "dite",]
        filtered_content = " ".join([word for word in lemmatized_content.split() if word not in stop_words])

        # Extraction des mots clés
        keywords = re.findall(r"\b[a-z0-9_-]+\b", filtered_content)

        
        
        # Insertion des mots clés dans la table `keywords`
        for keyword in keywords:
            if cursor.execute("SELECT COUNT(*) FROM keywords WHERE name = %s AND documents = %s", (keyword, document["name"])):
                count = cursor.fetchone()[0]

            if count > 0:
                continue
            if(keyword in mots_vides):
                continue
            if(len(keyword)<=2):
                continue
            if(keyword not in mots_vides):
                cursor.execute("INSERT INTO keywords (name, documents,title,description,pathtopdf) VALUES (%s, %s, %s, %s, %s)",(keyword, document["name"], document["title"], document["description"], document["pathtopdf"]))


    connection.commit()
    cursor.close()
    connection.close()

    return

def search(query):
    connection = MySQLdb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD, database=DB_DATABASE)
    cursor = connection.cursor()
    # Séparer le requete en des mots individuelle
    query_words = query.lower().split()
    # Cherchef chaque mot dans la table 'keywords'
    results = []
    for word in query_words:
        # obtenir les documents associés avec le mot
        cursor.execute("SELECT * FROM keywords WHERE name = %s", (word,))
        documents = cursor.fetchall()
        # Si le mot est trouvé, ajouter les informations liées au mot dans la liste 'results'
        if documents:
            for document in documents:
                if document[2] not in results:
                    results.append(document[2])
                if document[3] not in results:
                    results.append(document[3])
                if document[4] not in results:
                    results.append(document[4])
                if document[5] not in results:
                    results.append(document[5])
    return list(results)




documents = [

{
        "name": "document 1",
        "path": "C:\docs\doc1.txt",
         "title": "Intelligence artificielle et ecriture dynamique: De la raison graphique à la raison computationnelle - BACHIMONT Bruno",
        "description":"L’un des principaux attraits de l’informatique consiste en la possibilité qu’elle offre d’opérationaliser les connaissances dont on dispose sur un problème à résoudre ou une tâche à effectuer en un système automatique de résolution ou d’assistance à la résolution. C’est ainsi que l’informatique numérique offre des outils puissants pour opérationaliser des équations mathématiques décrivant un système physique, permettant ainsi de rendre effectif le modèle dont on dispose",
        "pathtopdf": "doc1"
    },
{
        "name": "document 2",
        "path": "C:\docs\doc2.txt",
         "title": "Chatbot et IA : Transformez votre Expérience Utilisateur",
        "description":"L'intelligence artificielle (IA) et les chatbots transactionnels continuent de redéfinir les interactions numériques, transformant profondément notre façon de communiquer, de travailler et de vivre. Avec des avancées significatives en traitement du langage naturel et en apprentissage automatique, les chatbots sont devenus plus sophistiqués, offrant des expériences personnalisées et interactives.",
        "pathtopdf": "doc2"
    },
    {
        "name": "document 3",
        "path": "C:\docs\doc3.txt",
         "title": "Intelligence artificielle, de quoi parle-t-on ?",
        "description":"L'intelligence artificielle (ou IA) est de plus en plus présente dans notre quotidien, notamment au travers de nouveaux produits ou services. Elle repose cependant sur des algorithmes gourmands en données, souvent personnelles, et son usage nécessite le respect de certaines précautions.",
        "pathtopdf": "doc3"
    },
    {
        "name": "document 4",
        "path": "C:\docs\doc4.txt",
         "title": "Qu'est ce que L'intelligence artificielle?",
        "description":"L'intelligence artificielle (IA) est un processus d'imitation de l'intelligence humaine qui repose sur la création et l'application d'algorithmes exécutés dans un environnement informatique dynamique. Son but est de permettre à des ordinateurs de penser et d'agir comme des êtres humains.",
        "pathtopdf": "doc4"
    },
    {
        "name": "document 5",
        "path": "C:\docs\doc5.txt",
         "title": "Intelligence artificielle : une mine d’or pour les entreprises",
        "description":"Les innovations rendues possibles grâce aux récents progrès de l’intelligence artificielle sont vastes et pourraient avoir des répercussions sociales et industrielles majeures. Qu’est-ce qui distingue les techniques de l’intelligence artificielle moderne? Comment les entreprises pourraient-elles bénéficier de ces avancées?",
        "pathtopdf": "doc5"
    },
    {
        "name": "document 6",
        "path": "C:\docs\doc6.txt",
         "title": "Apprentissage automatique",
        "description":"L'apprentissage automatique (en anglais : machine learning, litt. « apprentissage machine »), apprentissage artificiel ou apprentissage statistique est un champ d'étude de l'intelligence artificielle qui se fonde sur des approches mathématiques et statistiques pour donner aux ordinateurs la capacité d'« apprendre » à partir de données, c'est-à-dire d'améliorer leurs performances à résoudre des tâches sans être explicitement programmés pour chacune.",
        "pathtopdf": "doc6"
    },
    {
        "name": "document 7",
        "path": "C:\docs\doc7.txt",
         "title": "Grands modèles de langage",
        "description":"Un grand modèle de langage , grand modèle linguistique , grand modèle de langue , modèle de langage de grande taille ou encore modèle massif de langage (abrégé LLM de l'anglais large language model) est un modèle de langage possédant un grand nombre de paramètres (généralement de l'ordre du milliard de poids ou plus).",
        "pathtopdf": "doc7"
    },
    {
        "name": "document 9",
        "path": "C:\docs\doc9.txt",
         "title": "Histoire de l'intelligence artificielle - Intelligence artificielle",
        "description":"L’intelligence artificielle (IA) est une discipline jeune d’une soixante d’années, qui est un ensemble de sciences, théories et techniques (notamment logique mathématique, statistiques, probabilités, neurobiologie computationnelle, informatique) qui ambitionne d’imiter les capacités cognitives d’un être humain. Initiés dans le souffle de la seconde guerre mondiale, ses développements sont intimement liés à ceux de l’informatique et ont conduit les ordinateurs à réaliser des tâches de plus en plus complexes, qui ne pouvaient être auparavant que déléguées à un humain.",
        "pathtopdf": "doc9"
    },

    {
        "name": "document 10",
        "path": "C:\docs\doc10.txt",
         "title": "Qu’est-ce que l’apprentissage automatique ?",
        "description":"Une forme d’intelligence artificielle (IA) qui permet à un système d’apprendre de manière itérative à partir des données grâce à différents algorithmes pour les décrire et prévoir des résultats en apprenant à partir de données de formation qui génèrent des modèles précis.",
        "pathtopdf": "doc10"
    },
    {
        "name": "document 11",
        "path": "C:\docs\doc11.txt",
         "title": "Les types d’apprentissage automatique - Elements of AI",
        "description":"Les chiffres manuscrits sont un exemple classique souvent utilisé pour discuter des raisons pour lesquelles on fait appel à l’apprentissage automatique, et nous ne dérogerons pas à la règle. Vous trouverez ci-dessous des exemples d’images manuscrites provenant de la base de données MNIST, qui est très couramment utilisée.",
        "pathtopdf": "doc11"
    },


   

]


index_documents(documents)

app = Flask(__name__)



@app.route("/", methods=["POST","GET"])
def home():
    if request.method == "POST":
        query = request.form["nm"]
        results = search(query)
        n=len(results)
        return render_template("serp.html",results1=results,m=n,q=query)
    else :
        return render_template("index.html")

    
@app.route("/doc1")
def doc1():
    return render_template("doc1.html")

@app.route("/doc2")
def doc2():
    return render_template("doc2.html")
@app.route("/doc3")
def doc3():
    return render_template("doc3.html")

@app.route("/doc4")
def doc4():
    return render_template("doc4.html")

@app.route("/doc5")
def doc5():
    return render_template("doc5.html")

@app.route("/doc6")
def doc6():
    return render_template("doc6.html")

@app.route("/doc7")
def doc7():
    return render_template("doc7.html")
@app.route("/doc9")
def doc9():
    return render_template("doc9.html")
@app.route("/doc10")
def doc10():
    return render_template("doc10.html")
@app.route("/doc11")
def doc11():
    return render_template("doc11.html")
if __name__ == "__main_":

    app.run(debug=True)