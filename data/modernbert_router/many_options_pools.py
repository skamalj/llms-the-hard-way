"""Option pools for the many-option questions: one list of distinct values per topic, split into a TRAIN half and a TEST
half that share no value. The hand-written texts (many_options_train_texts.py, many_options_test_texts.py) name values from
their own half; the remaining options of a question are drawn from the same pool, so every option is the same kind of
thing as the answer (a city among cities), never a near-duplicate of another option."""

TRAIN = {
    "city": ["Lisbon", "Oslo", "Munich", "Prague", "Dublin", "Vienna", "Krakow", "Seville", "Porto", "Lyon", "Milan", "Naples",
             "Athens", "Helsinki", "Tallinn", "Riga", "Vilnius", "Zagreb", "Split", "Budapest", "Bucharest", "Sofia", "Valencia",
             "Bilbao", "Marseille", "Nice", "Geneva", "Zurich", "Hamburg", "Cologne", "Antwerp", "Rotterdam", "Copenhagen",
             "Gothenburg", "Bergen", "Reykjavik", "Edinburgh", "Cardiff", "Belfast", "Manchester", "Toronto", "Montreal", "Boston",
             "Chicago", "Denver", "Seattle", "Sydney", "Perth", "Auckland", "Cape Town", "Nairobi", "Lagos", "Mumbai", "Chennai",
             "Bangkok", "Hanoi", "Osaka", "Busan", "Lima", "Santiago"],
    "name": ["Amira", "Ben", "Chloe", "Daniel", "Elena", "Farid", "Grace", "Hugo", "Isla", "Jack", "Kemi", "Leo", "Maya", "Noah",
             "Olivia", "Pablo", "Quinn", "Rosa", "Samir", "Tara", "Umar", "Vera", "Will", "Yusuf", "Zoe", "Aaron", "Bella", "Callum",
             "Daisy", "Ethan", "Freya", "George", "Hannah", "Ibrahim", "Jade", "Kai", "Lily", "Max", "Nina", "Oscar", "Priya", "Rhys",
             "Sofia", "Tom", "Uma", "Victor", "Wendy", "Yasmin", "Zack", "Adam", "Beth", "Carlos", "Dina", "Eli", "Fiona", "Gabe",
             "Holly", "Ivan", "Julia", "Kevin"],
    "food": ["lasagne", "risotto", "fish and chips", "chicken tikka", "beef burrito", "veggie burger", "tomato soup", "greek salad",
             "pepperoni pizza", "spaghetti bolognese", "lamb kebab", "pad see ew", "chicken noodle soup", "falafel plate",
             "mushroom pie", "salmon fillet", "sausage and mash", "cottage pie", "pork ramen", "tuna sandwich", "egg fried rice",
             "chickpea curry", "steak pie", "cheese toastie", "club sandwich", "chicken wings", "vegetable soup", "beef chilli",
             "prawn cocktail", "fish curry", "lentil soup", "roast chicken", "pulled pork bun", "macaroni cheese", "jacket potato",
             "bean chilli", "fish finger sandwich", "chicken caesar wrap", "paneer tikka", "tofu curry", "seafood chowder",
             "beef lasagne", "spinach ravioli", "pea risotto", "chicken satay", "sweet potato curry", "mozzarella salad",
             "bacon roll", "pancakes", "porridge", "fruit salad", "apple crumble", "chocolate brownie", "lemon tart", "cheesecake"],
    "product": ["blender", "toaster", "desk lamp", "rice cooker", "kettle", "hair dryer", "electric fan", "standing mirror",
                "bath towel set", "duvet cover", "yoga mat", "dumbbell set", "rucksack", "umbrella", "wall clock", "picture frame",
                "coffee grinder", "cutlery set", "frying pan", "saucepan", "chopping board", "bread bin", "laundry basket",
                "ironing board", "bookshelf", "office chair", "bedside table", "shoe rack", "cushion cover", "table runner",
                "phone case", "power bank", "keyboard", "mouse pad", "webcam", "printer paper", "water bottle", "lunch box",
                "travel mug", "scented candle", "plant pot", "garden hose", "bird feeder", "tool box", "step ladder",
                "extension lead", "smoke alarm", "door mat", "shower curtain", "bath mat", "electric toothbrush", "hand mixer",
                "slippers", "bike helmet", "sun lounger"],
    "job": ["nurse", "plumber", "electrician", "accountant", "teacher", "chef", "pilot", "architect", "dentist", "vet", "lawyer",
            "journalist", "firefighter", "librarian", "pharmacist", "carpenter", "mechanic", "baker", "florist", "gardener",
            "photographer", "translator", "surveyor", "optician", "paramedic", "receptionist", "cleaner", "butcher", "tailor",
            "barber", "engineer", "scientist", "farmer", "fisherman", "sailor", "judge", "banker", "cashier", "courier",
            "bus driver", "painter", "actor", "singer", "dancer", "football coach", "referee", "midwife", "physiotherapist",
            "estate agent", "web developer"],
    "animal": ["dog", "cat", "rabbit", "hamster", "guinea pig", "parrot", "goldfish", "tortoise", "horse", "pony", "donkey",
               "goat", "sheep", "cow", "pig", "chicken", "duck", "goose", "fox", "badger", "hedgehog", "squirrel", "deer", "owl",
               "eagle", "robin", "swan", "frog", "snake", "lizard", "bat", "otter", "seal", "dolphin", "whale", "shark", "crab",
               "lobster", "bee", "butterfly", "spider", "snail", "mouse", "rat", "ferret"],
    "sport": ["football", "tennis", "cricket", "rugby", "golf", "swimming", "cycling", "running", "boxing", "judo", "karate",
              "badminton", "squash", "table tennis", "basketball", "volleyball", "netball", "hockey", "rowing", "sailing",
              "skiing", "snowboarding", "surfing", "climbing", "archery", "fencing", "gymnastics", "darts", "snooker", "bowls"],
    "language": ["Spanish", "French", "German", "Italian", "Portuguese", "Dutch", "Swedish", "Norwegian", "Danish", "Finnish",
                 "Polish", "Czech", "Greek", "Turkish", "Arabic", "Hindi", "Urdu", "Bengali", "Mandarin", "Cantonese", "Japanese",
                 "Korean", "Thai", "Vietnamese", "Indonesian", "Swahili", "Hebrew", "Russian", "Ukrainian", "Romanian"],
    "colour": ["red", "blue", "green", "yellow", "black", "white", "grey", "navy", "olive", "maroon", "teal", "beige", "cream",
               "pink", "purple", "orange", "brown", "silver", "gold", "turquoise", "lilac", "mustard", "coral", "charcoal", "ivory",
               "khaki", "burgundy", "mint", "peach", "lavender"],
    "time": [f"{h % 12 or 12}:{m:02d} {'am' if h < 12 else 'pm'}" for h in range(6, 24) for m in (0, 30)],
    "date": [f"{d}{'st' if d in (1, 21, 31) else 'nd' if d in (2, 22) else 'rd' if d in (3, 23) else 'th'} of {m}"
             for m in ["June", "July", "August", "September"] for d in (2, 5, 8, 11, 14, 17, 20, 23, 26, 29)],
    "number": [str(n) for n in range(1, 61)],
    "team": ["Accounts Receivable", "Shipping", "Warehouse", "Product Design", "Quality Control", "Customer Success", "Sales",
             "Partnerships", "Investor Relations", "Public Relations", "Security", "Cleaning Services", "Software Engineering",
             "Data Science", "Brand", "Social Media", "Office Management", "Returns Processing", "Fraud Prevention",
             "Credit Control", "Payroll Support", "Learning & Development", "Compliance", "Research", "Visitor Services",
             "Maintenance", "IT Helpdesk", "Purchasing", "Legal Affairs", "Events Team"],
}

TEST = {
    "city": ["Ljubljana", "Bratislava", "Salzburg", "Innsbruck", "Bologna", "Florence", "Turin", "Genoa", "Palermo", "Malaga",
             "Granada", "Cordoba", "Bordeaux", "Toulouse", "Nantes", "Strasbourg", "Lille", "Ghent", "Bruges", "Utrecht", "Leipzig",
             "Dresden", "Stuttgart", "Hanover", "Aarhus", "Malmo", "Uppsala", "Tampere", "Turku", "Gdansk", "Wroclaw", "Poznan",
             "Brno", "Debrecen", "Plovdiv", "Thessaloniki", "Izmir", "Valletta", "Nicosia", "Inverness", "Aberdeen", "Glasgow",
             "Leeds", "Bristol", "York", "Kyoto", "Pune", "Cusco", "Quito", "Hobart"],
    "name": ["Anika", "Bruno", "Celine", "Dmitri", "Esme", "Felix", "Gemma", "Hamid", "Ingrid", "Jonas", "Kirsty", "Lars", "Marta",
             "Nadia", "Otto", "Petra", "Rafael", "Saskia", "Tobias", "Ursula", "Vikram", "Wanda", "Yara", "Zainab", "Albert",
             "Beatrice", "Cyrus", "Delia", "Emil", "Flora", "Gustav", "Hedda", "Imogen", "Jorge", "Klara", "Lorenzo", "Mirela",
             "Nils", "Odile", "Piers", "Rania", "Stellan", "Thea", "Ulrich", "Valeria", "Wilf", "Ximena", "Yannick", "Zelda", "Agnes"],
    "food": ["mushroom stroganoff", "beef stew", "fish pie", "lamb tagine", "chicken korma", "vegetable moussaka", "pad thai",
             "caesar salad", "carrot soup", "seafood paella", "steak and chips", "falafel wrap", "beetroot salad", "pork belly",
             "duck confit", "prawn linguine", "cheese omelette", "nut roast", "chilli con carne", "shepherd's pie",
             "goat's cheese tart", "miso ramen", "sushi platter", "burrito bowl", "carbonara", "katsu curry", "fish tacos",
             "potato gnocchi", "spinach pie", "bean burger", "pea soup", "halloumi skewers", "crab cakes", "lentil dahl",
             "chicken kiev", "quiche lorraine", "sea bass", "tofu stir-fry", "beef burger", "eggs benedict", "french toast",
             "waffles", "rice pudding", "sticky toffee pudding", "tiramisu", "panna cotta", "bread and butter pudding",
             "banana split", "eton mess", "trifle"],
    "product": ["food processor", "slow cooker", "waffle maker", "juicer", "sandwich toaster", "air fryer", "stand mixer",
                "ice cream maker", "salad spinner", "casserole dish", "cake tin", "wok", "teapot", "spice rack", "wine rack",
                "coat stand", "floor lamp", "ceiling fan", "dehumidifier", "heated blanket", "weighted blanket", "pillow set",
                "mattress topper", "sleeping bag", "camping stove", "tent pegs", "hiking poles", "ski goggles", "swim cap",
                "tennis racket", "cricket bat", "golf umbrella", "bike lock", "car seat cover", "dash cam", "baby monitor",
                "high chair", "paddling pool", "garden bench", "compost bin", "hedge trimmer", "leaf blower", "pressure washer",
                "doorbell camera", "label printer"],
    "job": ["radiographer", "locksmith", "beekeeper", "glazier", "roofer", "plasterer", "tiler", "upholsterer", "cobbler",
            "jeweller", "watchmaker", "blacksmith", "stonemason", "welder", "crane operator", "air traffic controller",
            "lifeguard", "zookeeper", "park ranger", "sommelier", "barista", "auctioneer", "archivist", "curator",
            "cartographer", "geologist", "meteorologist", "astronomer", "statistician", "actuary", "auditor", "notary",
            "social worker", "speech therapist", "dietitian", "chiropodist", "dental hygienist", "occupational therapist",
            "anaesthetist", "sonographer", "tour guide", "dog groomer", "piano tuner", "chimney sweep", "window cleaner"],
    "animal": ["llama", "alpaca", "camel", "zebra", "giraffe", "elephant", "rhino", "hippo", "lion", "tiger", "leopard",
               "cheetah", "wolf", "bear", "panda", "koala", "kangaroo", "wombat", "platypus", "penguin", "flamingo", "pelican",
               "peacock", "toucan", "ostrich", "crocodile", "iguana", "chameleon", "gecko", "octopus", "squid", "jellyfish",
               "starfish", "seahorse", "walrus", "moose", "bison", "lynx", "raccoon", "skunk"],
    "sport": ["lacrosse", "handball", "water polo", "canoeing", "kayaking", "triathlon", "pentathlon", "curling", "bobsleigh",
              "ice hockey", "figure skating", "speed skating", "taekwondo", "wrestling", "weightlifting", "baseball", "softball",
              "polo", "croquet", "pickleball", "padel", "orienteering", "paragliding", "skateboarding", "BMX"],
    "language": ["Catalan", "Basque", "Welsh", "Irish", "Icelandic", "Estonian", "Latvian", "Lithuanian", "Slovak", "Slovenian",
                 "Croatian", "Serbian", "Bulgarian", "Hungarian", "Albanian", "Maltese", "Tamil", "Telugu", "Marathi", "Punjabi"],
    "colour": ["Harbour Mist", "Sage Leaf", "Desert Sand", "Midnight Ink", "Chalk Linen", "Copper Kettle", "Morning Fog",
               "Pine Forest", "Rose Quartz", "Storm Cloud", "Wheat Field", "Ocean Spray", "Lemon Sorbet", "Slate Roof",
               "Cinnamon Stick", "Arctic Ice", "Plum Velvet", "Honey Glow", "Moss Bank", "Pebble Beach", "Cherry Blossom",
               "Smoky Quartz", "Summer Sky", "Autumn Leaf", "Marble Hall", "Tea Rose", "Iron Gate", "Linen Sheet",
               "Saffron Thread", "Hazel Nut"],
    "time": [f"{h % 12 or 12}:{m:02d} {'am' if h < 12 else 'pm'}" for h in range(6, 24) for m in (15, 45)],
    "date": [f"{d} {m}" for m in ["January", "February", "March", "April", "May", "October", "November", "December"]
             for d in (3, 9, 16, 22, 28)],
    "number": [str(n) for n in range(1, 61)],
    "department": ["Payroll", "Legal", "Facilities", "IT Security", "Procurement", "Recruitment", "Travel Desk", "Health & Safety",
                   "Internal Comms", "Expenses", "Training", "Pensions", "Data Protection", "Reception", "Catering", "Fleet",
                   "Insurance", "Customer Complaints", "Marketing", "Translation", "Mailroom", "Archives", "Print Room",
                   "Car Parking", "Occupational Health", "Sustainability", "Internal Audit", "Tax", "Accounts Payable", "Events"],
}

# numbers are shared on purpose (they are not vocabulary); every other pool is disjoint between TRAIN and TEST
SHARED_OK = {"number"}


def check():
    for topic, values in list(TRAIN.items()) + list(TEST.items()):
        assert len(values) == len(set(values)), f"duplicate value in {topic}"
    for topic in TRAIN:
        if topic in TEST and topic not in SHARED_OK:
            shared = {v.lower() for v in TRAIN[topic]} & {v.lower() for v in TEST[topic]}
            assert not shared, f"{topic}: {shared}"


check()
