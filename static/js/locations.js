/**
 * Azoria - Bibliothèque Mondiale des Pays, Drapeaux & Données Géographiques
 * Inclut tous les pays avec drapeaux, indicatifs téléphoniques internationaux (+225, +33, +1...),
 * formats de numéros, et subdivisions détaillées (villes & communes) pour le commerce.
 */

(function () {
    const COUNTRIES = {
        // ─── AFRIQUE DE L'OUEST & CENTRALE ───
        "CI": {
            name: "Côte d'Ivoire",
            flag: "🇨🇮",
            dialCode: "+225",
            phonePlaceholder: "07 00 00 00 00",
            phoneLength: 10,
            currency: "FCFA",
            defaultCity: "Abidjan",
            cities: {
                "Abidjan": [
                    "Cocody (Angré, Riviera, 2 Plateaux, Danga...)",
                    "Yopougon (Selmer, Maroc, Niangon, Toit Rouge...)",
                    "Marcory (Zone 4, Biétry, Residentiel...)",
                    "Plateau (Centre des affaires)",
                    "Koumassi (Remblais, Soweto, Campement...)",
                    "Treichville (Arras, Avenue 8, Belleville...)",
                    "Adjamé (220 Logements, Liberté, Mirador...)",
                    "Abobo (Sogefiha, Abobo Baoulé, Samaké...)",
                    "Port-Bouët (Vridi, Gonzagueville, Derrière-rail...)",
                    "Attécoubé (Agban, Santé, Décon...)",
                    "Bingerville (Feh Kessé, Akandjé, Centre...)",
                    "Songon",
                    "Anyama"
                ],
                "Bouaké": ["Koko", "Nimbo", "Belleville", "Air France", "N'gattakro", "Broukro", "Commerce", "Ahougnanssou", "Autre quartier"],
                "Yamoussoukro": ["Morofé", "Assabou", "220 Logements", "Kokrenou", "Habitat", "Fondation", "N'zuessy", "Autre quartier"],
                "San-Pédro": ["Bardot", "Cité", "Séwéké", "Balmer", "Lac", "Zone Industrielle", "Autre quartier"],
                "Korhogo": ["Koko", "Petit Paris", "Sinistré", "Tchékélé", "Soba", "Kassirimé", "Autre quartier"],
                "Daloa": ["Tazibouo", "Lobia", "Marais", "Gbeuliville", "Commerce", "Autre quartier"],
                "Man": ["Grand Gbapleu", "Koko", "Domoraud", "Doyagouiné", "Sari", "Autre quartier"],
                "Grand-Bassam": ["Quartier France", "Moossou", "Impérial", "Rosiers", "Phare", "Autre quartier"],
                "Autres villes (Intérieur)": ["Soubré", "Gagnoa", "Abengourou", "Bondoukou", "Divo", "Agboville", "Ferkessédougou", "Adzopé", "Autre commune"]
            }
        },
        "SN": {
            name: "Sénégal",
            flag: "🇸🇳",
            dialCode: "+221",
            phonePlaceholder: "77 000 00 00",
            phoneLength: 9,
            currency: "FCFA",
            defaultCity: "Dakar",
            cities: {
                "Dakar": ["Dakar Plateau", "Almadies / Ngor", "Ouakam / Mamelles", "Mermoz / Sacré-Cœur", "Fann / Point E", "Médina / Gueule Tapée", "Yoff / Nord Foire", "Grand Yoff / Liberté", "Parcelles Assainies", "Pikine", "Guédiawaye", "Rufisque / Diamniadio"],
                "Thiès": ["Grand Thiès", "Mbour 1 / 2", "Randoulène", "Dixième", "Cité Lamy", "Autre quartier"],
                "Saint-Louis": ["Île de Saint-Louis", "Sor", "Balacoss", "Ndar Toute", "Pikine", "Autre quartier"],
                "Mbour / Saly": ["Saly Portudal", "Somone", "Ngaparou", "Grand Mbour", "Tefess", "Autre quartier"],
                "Touba / Mbacké": ["Touba Mosquée", "Darou Marnane", "Mbacké Centre", "Gouye Mbinde", "Autre quartier"],
                "Ziguinchor": ["Boucotte", "Santhiaba", "Lyndiane", "Kenia", "Autre quartier"],
                "Autres villes du Sénégal": ["Kaolack", "Kolda", "Tambacounda", "Louga", "Fatick", "Kédougou", "Autre localité"]
            }
        },
        "ML": {
            name: "Mali",
            flag: "🇲🇱",
            dialCode: "+223",
            phonePlaceholder: "70 00 00 00",
            phoneLength: 8,
            currency: "FCFA",
            defaultCity: "Bamako",
            cities: {
                "Bamako": ["Commune I (Korofina, Banconi)", "Commune II (Hippodrome, Médina)", "Commune III (Badiallan, Centre)", "Commune IV (Hamdallaye, ACI 2000, Lafiabougou)", "Commune V (Badalabougou, Baco Djicoroni)", "Commune VI (Sogoniko, Faladié, Yirimadio)"],
                "Sikasso": ["Wayerma", "Mancourani", "Mamelon", "Bougoula", "Autre quartier"],
                "Ségou": ["Ségou Koro", "Angoulême", "Pelengana", "Médine", "Autre quartier"],
                "Kayes": ["Kayes N'Di", "Légal Ségou", "Khasso", "Liberté", "Autre quartier"],
                "Autres villes du Mali": ["Mopti", "Koulikoro", "Gao", "Koutiala", "San", "Autre localité"]
            }
        },
        "BF": {
            name: "Burkina Faso",
            flag: "🇧🇫",
            dialCode: "+226",
            phonePlaceholder: "70 00 00 00",
            phoneLength: 8,
            currency: "FCFA",
            defaultCity: "Ouagadougou",
            cities: {
                "Ouagadougou": ["Ouaga 2000", "Koulouba / Centre-ville", "Gounghin", "Pissy", "Patte d'Oie", "Dassasgho", "Karpala", "Tampouy", "Saaba", "Somgandé"],
                "Bobo-Dioulasso": ["Bindougousso", "Sarfalao", "Koko", "Accart-ville", "Colma", "Lafiabougou", "Autre quartier"],
                "Koudougou": ["Secteur 1", "Secteur 2", "Palogo", "Burkindi", "Autre quartier"],
                "Autres villes du Burkina": ["Banfora", "Ouahigouya", "Fada N'Gourma", "Dédougou", "Kaya", "Autre localité"]
            }
        },
        "BJ": {
            name: "Bénin",
            flag: "🇧🇯",
            dialCode: "+229",
            phonePlaceholder: "97 00 00 00",
            phoneLength: 8,
            currency: "FCFA",
            defaultCity: "Cotonou",
            cities: {
                "Cotonou": ["Cadjèhoun / Haie Vive", "Akpakpa (Dodomè, PK6, Senadé)", "Gbégamey / Saint-Michel", "Fidjrossè / Plage", "Ménontin / Zogbo", "Kouhounou / Stade", "Vodjè / Maro-Militaire"],
                "Abomey-Calavi": ["Godomey / Togoudo", "Arconville", "Calavi Centre", "Tankpè", "Akassato", "Zinvié"],
                "Porto-Novo": ["Ouando", "Avakpa", "Djassin", "Attakè", "Dowa", "Autre quartier"],
                "Parakou": ["Albarika", "Camp Adagbè", "Zongo", "Banikanni", "Autre quartier"],
                "Autres villes du Bénin": ["Ouidah", "Bohicon", "Abomey", "Natitingou", "Djougou", "Autre localité"]
            }
        },
        "TG": {
            name: "Togo",
            flag: "🇹🇬",
            dialCode: "+228",
            phonePlaceholder: "90 00 00 00",
            phoneLength: 8,
            currency: "FCFA",
            defaultCity: "Lomé",
            cities: {
                "Lomé": ["Tokoin (Forever, Casablanca)", "Bè (Kpota, Beach)", "Nyékonakpoè / Kodjoviakopé", "Agoè-Nyivé (Assiyéyé)", "Hédzranawoé / Aéroport", "Baguida / Avépozo", "Adidogomé", "Kégué / Stade"],
                "Kara": ["Lama", "Chaminade", "Kpédah", "Tchintchinda", "Autre quartier"],
                "Sokodé": ["Didaouré", "Kparatao", "Komah", "Autre quartier"],
                "Kpalimé": ["Kpodzi", "Zomayi", "Nyivémé", "Kuma", "Autre quartier"],
                "Autres villes du Togo": ["Atakpamé", "Dapaong", "Tsévié", "Aného", "Autre localité"]
            }
        },
        "GN": {
            name: "Guinée",
            flag: "🇬🇳",
            dialCode: "+224",
            phonePlaceholder: "620 00 00 00",
            phoneLength: 9,
            currency: "GNF",
            defaultCity: "Conakry",
            cities: {
                "Conakry": ["Kaloum (Centre-ville)", "Dixinn (Minière, Camayenne)", "Matam (Madina, Bonfi)", "Ratoma (Kipé, Nongo, Lambanyi)", "Matoto (Yimbaya, Entag, Gbessia)"],
                "Kindia": ["Tafory", "Manquepas", "Autre quartier"],
                "Kankan": ["Bordo", "Missira", "Autre quartier"],
                "Labé": ["Pounthioun", "Daka", "Autre quartier"],
                "Autres villes de Guinée": ["Nzérékoré", "Mamou", "Boké", "Faranah", "Kamsar", "Autre localité"]
            }
        },
        "NE": {
            name: "Niger",
            flag: "🇳🇪",
            dialCode: "+227",
            phonePlaceholder: "90 00 00 00",
            phoneLength: 8,
            currency: "FCFA",
            defaultCity: "Niamey",
            cities: {
                "Niamey": ["Niamey I (Plateau, Yantala)", "Niamey II (Boukoki, Talladjé)", "Niamey III (Koira Kano)", "Niamey IV (Gamkalley, Aéroport)", "Niamey V (Harobanda)"],
                "Maradi": ["Ali Dan Sofo", "Zaria", "Autre quartier"],
                "Zinder": ["Birni", "Zengou", "Autre quartier"],
                "Autres villes du Niger": ["Tahoua", "Agadez", "Dosso", "Diffa", "Tillabéri", "Autre localité"]
            }
        },
        "CM": {
            name: "Cameroun",
            flag: "🇨🇲",
            dialCode: "+237",
            phonePlaceholder: "6 00 00 00 00",
            phoneLength: 9,
            currency: "FCFA",
            defaultCity: "Douala",
            cities: {
                "Douala": ["Akwa", "Bonanjo", "Bonapriso", "Bali", "Deido", "Makepe", "Bonamoussadi", "Logpom", "Bépanda", "Ndogbong", "Yassa", "Autre quartier"],
                "Yaoundé": ["Bastos", "Centre-ville", "Omnisports", "Mimboman", "Biyem-Assi", "Mendong", "Ngousso", "Emana", "Nkolbisson", "Autre quartier"],
                "Bafoussam": ["Djeleng", "Toukouop", "Tamda", "Autre quartier"],
                "Garoua": ["Bibémiré", "Poumpoumré", "Laindé", "Autre quartier"],
                "Autres villes du Cameroun": ["Bamenda", "Kribi", "Limbe", "Maroua", "Ngaoundéré", "Bertoua", "Ebolowa", "Autre localité"]
            }
        },
        "GA": {
            name: "Gabon",
            flag: "🇬🇦",
            dialCode: "+241",
            phonePlaceholder: "74 00 00 00",
            phoneLength: 8,
            currency: "FCFA",
            defaultCity: "Libreville",
            cities: {
                "Libreville": ["Centre-ville", "Akanda", "Louis", "Montagne Sainte", "Batterie IV", "Glass", "Oloumi", "Nzeng-Ayong", "PK5 / PK12", "Charbonnages", "Autre quartier"],
                "Port-Gentil": ["Matanda", "Grand Village", "Chavane", "Autre quartier"],
                "Franceville": ["Potos", "Mboumba", "Autre quartier"],
                "Autres villes du Gabon": ["Oyem", "Moanda", "Mouila", "Lambaréné", "Autre localité"]
            }
        },
        "CD": {
            name: "RD Congo",
            flag: "🇨🇩",
            dialCode: "+243",
            phonePlaceholder: "81 000 00 00",
            phoneLength: 9,
            currency: "USD / CDF",
            defaultCity: "Kinshasa",
            cities: {
                "Kinshasa": ["Gombe", "Ngaliema (Ma Campagne)", "Kintambo", "Lingwala", "Barumbu", "Kinshasa", "Limete", "Bandalungwa", "Kalamu (Matonge)", "Lemba", "Mont-Ngafula", "Masina", "Ndjili"],
                "Lubumbashi": ["Commune de Lubumbashi", "Kampemba", "Kenya", "Katuba", "Rwashi", "Annexe", "Autre quartier"],
                "Goma": ["Goma", "Karisimbi", "Himbi", "Kyeshero", "Autre quartier"],
                "Autres villes de RDC": ["Kolwezi", "Kisangani", "Bukavu", "Matadi", "Mbuji-Mayi", "Kananga", "Autre localité"]
            }
        },
        "CG": {
            name: "Congo-Brazzaville",
            flag: "🇨🇬",
            dialCode: "+242",
            phonePlaceholder: "06 000 00 00",
            phoneLength: 9,
            currency: "FCFA",
            defaultCity: "Brazzaville",
            cities: {
                "Brazzaville": ["Bacongo", "Poto-Poto", "Moungali", "Ouenzé", "Talangaï", "Makélékélé", "Mfilou", "Madibou", "Djiri"],
                "Pointe-Noire": ["Lumumba", "Mvoumvou", "Tié-Tié", "Loandjili", "Mongo-Mpoukou", "Ngoyo"],
                "Autres villes du Congo": ["Dolisie", "Nkayi", "Ouesso", "Owando", "Autre localité"]
            }
        },
        "GH": {
            name: "Ghana",
            flag: "🇬🇭",
            dialCode: "+233",
            phonePlaceholder: "24 000 0000",
            phoneLength: 9,
            currency: "GHS",
            defaultCity: "Accra",
            cities: {
                "Accra": ["Osu", "Airport Residential", "East Legon", "Cantonments", "Labone", "Dzorwulu", "Tema", "Spintex", "Madina", "Dansoman", "Kaneshie"],
                "Kumasi": ["Adum", "Nhyiaeso", "Asokwa", "Bantama", "Ahodwo", "Autre quartier"],
                "Autres villes du Ghana": ["Takoradi", "Tamale", "Cape Coast", "Sunyani", "Koforidua", "Autre localité"]
            }
        },
        "NG": {
            name: "Nigeria",
            flag: "🇳🇬",
            dialCode: "+234",
            phonePlaceholder: "803 000 0000",
            phoneLength: 10,
            currency: "NGN",
            defaultCity: "Lagos",
            cities: {
                "Lagos": ["Victoria Island", "Ikoyi", "Lekki Phase 1", "Ajah", "Ikeja (GRA)", "Surulere", "Yaba", "Maryland", "Gbagada", "Festac", "Ikorodu"],
                "Abuja": ["Maitama", "Asokoro", "Wuse 2", "Garki", "Jabi", "Gwarinpa", "Utako", "Guzape", "Autre quartier"],
                "Port Harcourt": ["Old GRA", "New GRA", "Trans Amadi", "Rumuokoro", "Autre quartier"],
                "Ibadan": ["Bodija", "Dugbe", "Ring Road", "Oluyole", "Autre quartier"],
                "Kano": ["Nassarawa", "Fagge", "Tarauni", "Autre quartier"]
            }
        },
        "TD": {
            name: "Tchad",
            flag: "🇹🇩",
            dialCode: "+235",
            phonePlaceholder: "66 00 00 00",
            phoneLength: 8,
            currency: "FCFA",
            defaultCity: "N'Djamena",
            cities: {
                "N'Djamena": ["1er Arrondissement (Farcha)", "2e Arrondissement (Bololo)", "3e Arrondissement (Ardep Djoumal)", "4e Arrondissement", "6e Arrondissement", "7e Arrondissement (Chagoua, Dembé)", "8e Arrondissement", "9e Arrondissement (Walila)"],
                "Moundou": ["Dombao", "Kouh", "Gueldjem", "Autre quartier"],
                "Autres villes du Tchad": ["Sarh", "Abéché", "Kélo", "Am Timan", "Autre localité"]
            }
        },
        "MR": {
            name: "Mauritanie",
            flag: "🇲🇷",
            dialCode: "+222",
            phonePlaceholder: "45 00 00 00",
            phoneLength: 8,
            currency: "MRU",
            defaultCity: "Nouakchott",
            cities: {
                "Nouakchott": ["Tevragh-Zeina", "Ksar", "Sebkha", "El Mina", "Arafat", "Dar-Naim", "Teyarett", "Toujounine", "Riyadh"],
                "Nouadhibou": ["Cansado", "Kran", "Numerowatt", "Autre quartier"],
                "Autres villes de Mauritanie": ["Rosso", "Kiffa", "Kaédi", "Atar", "Autre localité"]
            }
        },
        "RW": {
            name: "Rwanda",
            flag: "🇷🇼",
            dialCode: "+250",
            phonePlaceholder: "780 000 000",
            phoneLength: 9,
            currency: "RWF",
            defaultCity: "Kigali",
            cities: {
                "Kigali": ["Nyarugenge (Kiyovu, Nyamirambo)", "Gasabo (Kacyiru, Kimihurura, Nyarutarama, Gisozi, Kibagabaga)", "Kicukiro (Kanombe, Kagarama, Niboye)"],
                "Autres villes du Rwanda": ["Gisenyi (Rubavu)", "Musanze (Ruhengeri)", "Huye (Butare)", "Muhanga", "Autre localité"]
            }
        },
        "MA": {
            name: "Maroc",
            flag: "🇲🇦",
            dialCode: "+212",
            phonePlaceholder: "600 000 000",
            phoneLength: 9,
            currency: "MAD",
            defaultCity: "Casablanca",
            cities: {
                "Casablanca": ["Maârif / Gauthier", "Anfa / Ain Diab", "Bourgogne", "Sidi Maârouf", "Oasis / Californie", "Habous", "Ain Sebaa", "Mohammedia"],
                "Rabat": ["Agdal", "Souissi", "Hassan", "Hay Riad", "Océan", "Salé"],
                "Marrakech": ["Guéliz", "Hivernage", "Médina", "Palmeraie", "Targa", "Mhamid"],
                "Tanger": ["Malabata", "Centre", "Boubana", "California", "Iberia", "Médina"],
                "Autres villes du Maroc": ["Fès", "Agadir", "Meknès", "Oujda", "Tétouan", "Kénitra", "El Jadida", "Nador", "Autre localité"]
            }
        },
        "TN": {
            name: "Tunisie",
            flag: "🇹🇳",
            dialCode: "+216",
            phonePlaceholder: "20 000 000",
            phoneLength: 8,
            currency: "TND",
            defaultCity: "Tunis",
            cities: {
                "Tunis": ["Centre-ville", "Les Berges du Lac 1 / 2", "La Marsa", "Carthage / Sidi Bou Saïd", "Menzah / Manar", "Ennasr", "Ariana"],
                "Sousse": ["Kantaoui", "Sousse Ville", "Hammam Sousse", "Sahloul", "Autre quartier"],
                "Sfax": ["Sfax Ville", "Route de Téniour", "Route de Tunis", "Autre quartier"],
                "Autres villes de Tunisie": ["Monastir", "Bizerte", "Nabeul / Hammamet", "Gabès", "Kairouan", "Djerba", "Autre localité"]
            }
        },
        "DZ": {
            name: "Algérie",
            flag: "🇩🇿",
            dialCode: "+213",
            phonePlaceholder: "550 00 00 00",
            phoneLength: 9,
            currency: "DZD",
            defaultCity: "Alger",
            cities: {
                "Alger": ["Alger-Centre", "Hydra", "El Biar", "Ben Aknoun", "Kouba", "Dely Ibrahim", "Bab El Oued", "Chéraga", "Hussein Dey", "Bordj El Kiffan"],
                "Oran": ["Akid Lotfi", "Centre-ville", "Maraval", "Canastel", "Seddikia", "Autre quartier"],
                "Constantine": ["Sidi Mabrouk", "Cité Bellevue", "Zouaghi", "Ali Mendjeli", "Autre quartier"],
                "Autres villes d'Algérie": ["Annaba", "Blida", "Batna", "Sétif", "Tlemcen", "Béjaïa", "Biskra", "Autre localité"]
            }
        },
        "EG": {
            name: "Égypte",
            flag: "🇪🇬",
            dialCode: "+20",
            phonePlaceholder: "100 000 0000",
            phoneLength: 10,
            currency: "EGP",
            defaultCity: "Le Caire",
            cities: {
                "Le Caire": ["Zamalek", "Maadi", "Heliopolis", "Nasr City", "New Cairo / 5th Settlement", "Downtown", "Garden City", "Sheikh Zayed / 6th of October"],
                "Alexandrie": ["Gleem", "Smouha", "Roushdy", "Stanley", "Montaza", "Autre quartier"],
                "Autres villes d'Égypte": ["Gizeh", "Louxor", "Assouan", "Charm el-Cheikh", "Hurghada", "Port-Saïd", "Autre localité"]
            }
        },
        "KE": {
            name: "Kenya",
            flag: "🇰🇪",
            dialCode: "+254",
            phonePlaceholder: "700 000 000",
            phoneLength: 9,
            currency: "KES",
            defaultCity: "Nairobi",
            cities: {
                "Nairobi": ["Westlands", "Kilimani", "Kileleshwa", "Karen", "Lavington", "Parklands", "CBD", "South B / C", "Runda", "Kasarani"],
                "Mombasa": ["Nyali", "Old Town", "Bamburi", "Kizingo", "Autre quartier"],
                "Autres villes du Kenya": ["Kisumu", "Nakuru", "Eldoret", "Thika", "Malindi", "Autre localité"]
            }
        },
        "ZA": {
            name: "Afrique du Sud",
            flag: "🇿🇦",
            dialCode: "+27",
            phonePlaceholder: "71 000 0000",
            phoneLength: 9,
            currency: "ZAR",
            defaultCity: "Johannesburg",
            cities: {
                "Johannesburg": ["Sandton", "Rosebank", "Fourways", "Randburg", "Midrand", "Braamfontein", "Soweto"],
                "Le Cap (Cape Town)": ["City Bowl", "Camps Bay", "Sea Point", "Green Point", "Claremont", "Constantia", "Century City"],
                "Durban": ["Umhlanga", "Morningside", "Berea", "Durban North", "Westville"],
                "Pretoria": ["Brooklyn", "Hatfield", "Menlyn", "Waterkloof", "Centurion"],
                "Autres villes d'Afrique du Sud": ["Gqeberha (Port Elizabeth)", "Bloemfontein", "East London", "Polokwane", "Nelspruit", "Autre localité"]
            }
        },
        "MG": {
            name: "Madagascar",
            flag: "🇲🇬",
            dialCode: "+261",
            phonePlaceholder: "32 00 000 00",
            phoneLength: 9,
            currency: "MGA",
            defaultCity: "Antananarivo",
            cities: {
                "Antananarivo": ["Analakely", "Ankorondrano", "Ivandry", "Isoraka", "Ambohimanarina", "Tanjombato", "Ambatobe"],
                "Toamasina (Tamatave)": ["Centre-ville", "Bazar Be", "Bazarikely", "Autre quartier"],
                "Autres villes de Madagascar": ["Antsirabe", "Mahajanga", "Fianarantsoa", "Nosy Be", "Toliara", "Antsiranana", "Autre localité"]
            }
        },
        "MU": {
            name: "Maurice",
            flag: "🇲🇺",
            dialCode: "+230",
            phonePlaceholder: "5000 0000",
            phoneLength: 8,
            currency: "MUR",
            defaultCity: "Port-Louis",
            cities: {
                "Port-Louis": ["Centre", "Plaine Verte", "Caudan", "Autre quartier"],
                "Grand Baie": ["Péreybère", "Mont Choisy", "Pointe aux Canonniers"],
                "Curepipe": ["Centre", "Floreal", "Forest Side"],
                "Autres localités": ["Flic en Flac", "Tamarin", "Quatre Bornes", "Rose Hill", "Beau Bassin", "Mahébourg"]
            }
        },

        // ─── EUROPE & AMÉRIQUE DU NORD ───
        "FR": {
            name: "France",
            flag: "🇫🇷",
            dialCode: "+33",
            phonePlaceholder: "06 00 00 00 00",
            phoneLength: 10,
            currency: "EUR",
            defaultCity: "Paris",
            cities: {
                "Paris": ["Paris 1er à 4e (Centre)", "Paris 8e / 9e (Opéra, Champs-Élysées)", "Paris 11e / 12e (Bastille, Nation)", "Paris 15e / 16e (Tour Eiffel, Passy)", "Paris 17e / 18e (Montmartre)", "Île-de-France (92, 93, 94, 78, 91, 77, 95)"],
                "Lyon": ["Presqu'île (1er, 2e)", "Part-Dieu (3e)", "Croix-Rousse (4e)", "Vieux Lyon (5e)", "Gerland (7e)", "Villeurbanne"],
                "Marseille": ["Vieux-Port", "Prado / Périer", "La Valentine", "Joliette", "Castellane", "Autre quartier"],
                "Autres villes de France": ["Toulouse", "Nice", "Nantes", "Montpellier", "Strasbourg", "Bordeaux", "Lille", "Rennes", "Reims", "Toulon", "Grenoble", "Dijon", "Autre ville"]
            }
        },
        "BE": {
            name: "Belgique",
            flag: "🇧🇪",
            dialCode: "+32",
            phonePlaceholder: "0470 00 00 00",
            phoneLength: 9,
            currency: "EUR",
            defaultCity: "Bruxelles",
            cities: {
                "Bruxelles": ["Bruxelles-Ville (Centre)", "Ixelles (Flagey, Châtelain)", "Uccle", "Etterbeek", "Saint-Gilles", "Schaerbeek", "Woluwe", "Anderlecht"],
                "Autres villes de Belgique": ["Anvers (Antwerpen)", "Gand (Gent)", "Liège", "Charleroi", "Bruges (Brugge)", "Namur", "Mons", "Louvain", "Tournai", "Autre ville"]
            }
        },
        "CH": {
            name: "Suisse",
            flag: "🇨🇭",
            dialCode: "+41",
            phonePlaceholder: "079 000 00 00",
            phoneLength: 9,
            currency: "CHF",
            defaultCity: "Genève",
            cities: {
                "Genève": ["Centre / Rive", "Eaux-Vives", "Plainpalais", "Pâquis / Nations", "Carouge", "Servette", "Autre quartier"],
                "Lausanne": ["Centre", "Ouchy", "Flon", "Chailly", "Sous-Gare", "Autre quartier"],
                "Zurich": ["Altstadt", "Zürich West", "Wiedikon", "Enge", "Oerlikon"],
                "Autres villes de Suisse": ["Bâle (Basel)", "Berne", "Lucerne", "Fribourg", "Neuchâtel", "Sion", "Lugano", "Autre ville"]
            }
        },
        "CA": {
            name: "Canada",
            flag: "🇨🇦",
            dialCode: "+1",
            phonePlaceholder: "(514) 000-0000",
            phoneLength: 10,
            currency: "CAD",
            defaultCity: "Montréal",
            cities: {
                "Montréal": ["Plateau-Mont-Royal", "Ville-Marie (Centre-ville)", "Côte-des-Neiges / NDG", "Rosemont / La Petite-Patrie", "Villeray / Saint-Michel", "Verdun / Sud-Ouest", "Laval / Rive-Nord", "Longueuil / Rive-Sud"],
                "Québec": ["Vieux-Québec", "Sainte-Foy", "Beauport", "Charlesbourg", "Limoilou"],
                "Toronto": ["Downtown", "Midtown", "North York", "Scarborough", "Etobicoke", "Mississauga"],
                "Autres villes du Canada": ["Ottawa / Gatineau", "Vancouver", "Calgary", "Edmonton", "Winnipeg", "Halifax", "Autre ville"]
            }
        },
        "US": {
            name: "États-Unis",
            flag: "🇺🇸",
            dialCode: "+1",
            phonePlaceholder: "(555) 000-0000",
            phoneLength: 10,
            currency: "USD",
            defaultCity: "New York",
            cities: {
                "New York": ["Manhattan", "Brooklyn", "Queens", "The Bronx", "Staten Island"],
                "Grandes métropoles": ["Los Angeles", "Chicago", "Houston", "Miami", "Atlanta", "Dallas", "Washington D.C.", "San Francisco", "Boston", "Seattle", "Autre ville"]
            }
        },
        "GB": {
            name: "Royaume-Uni",
            flag: "🇬🇧",
            dialCode: "+44",
            phonePlaceholder: "07000 000000",
            phoneLength: 10,
            currency: "GBP",
            defaultCity: "Londres",
            cities: {
                "Londres": ["Central London", "West London", "East London", "North London", "South London"],
                "Grandes villes": ["Manchester", "Birmingham", "Leeds", "Glasgow", "Liverpool", "Edinburgh", "Bristol", "Autre ville"]
            }
        },
        "AE": {
            name: "Émirats Arabes Unis",
            flag: "🇦🇪",
            dialCode: "+971",
            phonePlaceholder: "50 000 0000",
            phoneLength: 9,
            currency: "AED",
            defaultCity: "Dubaï",
            cities: {
                "Dubaï": ["Downtown / Business Bay", "Dubai Marina / JBR", "Deira", "Bur Dubai", "Jumeirah", "Al Barsha", "Palm Jumeirah"],
                "Abou Dabi": ["Corniche", "Al Reem Island", "Khalidiya", "Yas Island", "Autre quartier"],
                "Autres Émirats": ["Sharjah", "Ajman", "Ras Al Khaimah", "Fujairah", "Umm Al Quwain"]
            }
        },
        "CN": {
            name: "Chine",
            flag: "🇨🇳",
            dialCode: "+86",
            phonePlaceholder: "138 0000 0000",
            phoneLength: 11,
            currency: "CNY",
            defaultCity: "Guangzhou (Canton)",
            cities: {
                "Pôles Commerciaux": ["Guangzhou (Canton)", "Yiwu", "Shenzhen", "Shanghai", "Beijing (Pékin)", "Hong Kong", "Hangzhou", "Foshan", "Dongguan", "Autre ville"]
            }
        },
        "TR": {
            name: "Turquie",
            flag: "🇹🇷",
            dialCode: "+90",
            phonePlaceholder: "500 000 0000",
            phoneLength: 10,
            currency: "TRY",
            defaultCity: "Istanbul",
            cities: {
                "Istanbul": ["Fatih / Laleli (Commerce)", "Taksim / Beyoğlu", "Şişli / Osmanbey", "Kadıköy", "Bakırköy", "Zeytinburnu", "Autre quartier"],
                "Autres villes": ["Ankara", "Izmir", "Bursa", "Antalya", "Gaziantep", "Autre ville"]
            }
        },
        "HT": {
            name: "Haïti",
            flag: "🇭🇹",
            dialCode: "+509",
            phonePlaceholder: "34 00 0000",
            phoneLength: 8,
            currency: "HTG",
            defaultCity: "Port-au-Prince",
            cities: {
                "Port-au-Prince": ["Pétion-Ville", "Delmas", "Centre-ville", "Carrefour", "Tabarre", "Plaine du Cul-de-Sac"],
                "Autres villes": ["Cap-Haïtien", "Les Cayes", "Gonaïves", "Jacmel", "Saint-Marc", "Autre localité"]
            }
        },
        "DE": { name: "Allemagne", flag: "🇩🇪", dialCode: "+49", phonePlaceholder: "0151 00000000", phoneLength: 11, defaultCity: "Berlin", cities: { "Berlin": ["Mitte", "Charlottenburg", "Kreuzberg"], "Grandes villes": ["Munich", "Francfort", "Hambourg", "Cologne", "Düsseldorf", "Stuttgart", "Autre ville"] } },
        "IT": { name: "Italie", flag: "🇮🇹", dialCode: "+39", phonePlaceholder: "320 000 0000", phoneLength: 10, defaultCity: "Rome", cities: { "Rome": ["Centre", "EUR", "Prati"], "Grandes villes": ["Milan", "Naples", "Turin", "Florence", "Bologne", "Palerme", "Venise", "Autre ville"] } },
        "ES": { name: "Espagne", flag: "🇪🇸", dialCode: "+34", phonePlaceholder: "600 000 000", phoneLength: 9, defaultCity: "Madrid", cities: { "Madrid": ["Centro", "Salamanca", "Chamberí"], "Grandes villes": ["Barcelone", "Valence", "Séville", "Malaga", "Bilbao", "Alicante", "Autre ville"] } },
        "PT": { name: "Portugal", flag: "🇵🇹", dialCode: "+351", phonePlaceholder: "910 000 000", phoneLength: 9, defaultCity: "Lisbonne", cities: { "Lisbonne": ["Baixa", "Chiado", "Parque das Nações"], "Grandes villes": ["Porto", "Braga", "Coimbra", "Faro", "Funchal", "Autre ville"] } },
        "NL": { name: "Pays-Bas", flag: "🇳🇱", dialCode: "+31", phonePlaceholder: "06 00000000", phoneLength: 9, defaultCity: "Amsterdam", cities: { "Amsterdam": ["Centrum", "Zuid", "West"], "Grandes villes": ["Rotterdam", "La Haye (Den Haag)", "Utrecht", "Eindhoven", "Autre ville"] } },
        "LU": { name: "Luxembourg", flag: "🇱🇺", dialCode: "+352", phonePlaceholder: "621 000 000", phoneLength: 9, defaultCity: "Luxembourg", cities: { "Luxembourg": ["Ville-Haute", "Kirchberg", "Gare", "Limpertsberg"], "Autres communes": ["Esch-sur-Alzette", "Differdange", "Dudelange", "Autre commune"] } },
        "BR": { name: "Brésil", flag: "🇧🇷", dialCode: "+55", phonePlaceholder: "(11) 90000-0000", phoneLength: 11, defaultCity: "São Paulo", cities: { "Grandes villes": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Belo Horizonte", "Fortaleza", "Curitiba", "Autre ville"] } },
        "IN": { name: "Inde", flag: "🇮🇳", dialCode: "+91", phonePlaceholder: "98000 00000", phoneLength: 10, defaultCity: "Mumbai (Bombay)", cities: { "Grandes métropoles": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Ahmedabad", "Autre ville"] } },
        "JP": { name: "Japon", flag: "🇯🇵", dialCode: "+81", phonePlaceholder: "090-0000-0000", phoneLength: 10, defaultCity: "Tokyo", cities: { "Tokyo": ["Shinjuku", "Shibuya", "Minato", "Ginza"], "Grandes villes": ["Osaka", "Yokohama", "Kyoto", "Nagoya", "Fukuoka", "Sapporo", "Autre ville"] } },
        "LB": { name: "Liban", flag: "🇱🇧", dialCode: "+961", phonePlaceholder: "03 000 000", phoneLength: 8, defaultCity: "Beyrouth", cities: { "Beyrouth": ["Achrafieh", "Hamra", "Verdun", "Centre-ville"], "Autres villes": ["Tripoli", "Jounieh", "Saïda", "Byblos (Jbeil)", "Zahlé", "Autre ville"] } },
        "SA": { name: "Arabie Saoudite", flag: "🇸🇦", dialCode: "+966", phonePlaceholder: "50 000 0000", phoneLength: 9, defaultCity: "Riyad", cities: { "Riyad": ["Al Olaya", "Al Malqa", "Diplomatic Quarter"], "Grandes villes": ["Djeddah", "La Mecque", "Médine", "Dammam", "Khobar", "Autre ville"] } },
        "QA": { name: "Qatar", flag: "🇶🇦", dialCode: "+974", phonePlaceholder: "3000 0000", phoneLength: 8, defaultCity: "Doha", cities: { "Doha": ["West Bay", "The Pearl", "Lusail", "Al Sadd"], "Autres municipalités": ["Al Rayyan", "Al Wakrah", "Al Khor", "Autre commune"] } },
        "KW": { name: "Koweït", flag: "🇰🇼", dialCode: "+965", phonePlaceholder: "5000 0000", phoneLength: 8, defaultCity: "Koweït City", cities: { "Koweït City": ["Salmiya", "Hawalli", "Sharq"], "Autres gouvernorats": ["Ahmadi", "Farwaniya", "Jahra", "Mubarak Al-Kabeer"] } },
        "AO": { name: "Angola", flag: "🇦🇴", dialCode: "+244", phonePlaceholder: "923 000 000", phoneLength: 9, defaultCity: "Luanda", cities: { "Luanda": ["Ingombota", "Maianga", "Talatona", "Kilamba"], "Autres villes": ["Benguela", "Huambo", "Lobito", "Lubango", "Cabinda", "Autre ville"] } },
        "MZ": { name: "Mozambique", flag: "🇲🇿", dialCode: "+258", phonePlaceholder: "84 000 0000", phoneLength: 9, defaultCity: "Maputo", cities: { "Maputo": ["Polana", "Sommerschield", "Central"], "Autres villes": ["Matola", "Beira", "Nampula", "Tete", "Pemba", "Autre ville"] } },
        "CV": { name: "Cap-Vert", flag: "🇨🇻", dialCode: "+238", phonePlaceholder: "990 00 00", phoneLength: 7, defaultCity: "Praia", cities: { "Île de Santiago": ["Praia (Centre, Palmarejo, Achada)", "Assomada", "Tarrafal"], "Île de São Vicente": ["Mindelo"], "Île de Sal": ["Santa Maria", "Espargos"], "Autres îles": ["Boa Vista", "Fogo", "Santo Antão", "Autre île"] } },
        "GQ": { name: "Guinée Équatoriale", flag: "🇬🇶", dialCode: "+240", phonePlaceholder: "222 00 00 00", phoneLength: 9, defaultCity: "Malabo", cities: { "Malabo": ["Centre", "Ela Nguema", "Caracolas"], "Bata": ["Centre", "Nkolombong", "Comandachina"], "Autres villes": ["Mongomo", "Ebebiyin", "Oyala (Ciudad de la Paz)"] } },
        "CF": { name: "Centrafrique", flag: "🇨🇫", dialCode: "+236", phonePlaceholder: "75 00 00 00", phoneLength: 8, defaultCity: "Bangui", cities: { "Bangui": ["1er Arrondissement", "2e Arrondissement", "3e Arrondissement (PK5)", "4e Arrondissement", "5e Arrondissement", "6e Arrondissement", "7e Arrondissement", "8e Arrondissement"], "Autres villes": ["Bimbo", "Berbérati", "Carnot", "Bambari", "Bouar", "Autre ville"] } },
        "KM": { name: "Comores", flag: "🇰🇲", dialCode: "+269", phonePlaceholder: "320 00 00", phoneLength: 7, defaultCity: "Moroni", cities: { "Grande Comore": ["Moroni (Centre, Mtsangani, Badjanani)", "Mitsamiouli", "Foumbouni"], "Anjouan": ["Mutsamudu", "Domoni"], "Mohéli": ["Fomboni"] } },
        "DJ": { name: "Djibouti", flag: "🇩🇯", dialCode: "+253", phonePlaceholder: "77 00 00 00", phoneLength: 8, defaultCity: "Djibouti", cities: { "Djibouti-Ville": ["Ras Dika", "Boulaos", "Balbala", "Heron"], "Autres régions": ["Ali Sabieh", "Tadjourah", "Obock", "Dikhil", "Arta"] } },
        "ET": { name: "Éthiopie", flag: "🇪🇹", dialCode: "+251", phonePlaceholder: "91 000 0000", phoneLength: 9, defaultCity: "Addis-Abeba", cities: { "Addis-Abeba": ["Bole", "Kirkos", "Yeka", "Arada", "Lideta", "Nifas Silk"], "Autres villes": ["Dire Dawa", "Hawassa", "Bahir Dar", "Mekele", "Adama (Nazret)", "Gondar", "Autre ville"] } },
        "UG": { name: "Ouganda", flag: "🇺🇬", dialCode: "+256", phonePlaceholder: "770 000 000", phoneLength: 9, defaultCity: "Kampala", cities: { "Kampala": ["Central", "Nakawa (Bugolobi, Ntinda)", "Makindye (Kabalagala)", "Kawempe", "Rubaga"], "Autres villes": ["Entebbe", "Jinja", "Mbarara", "Gulu", "Mukono", "Autre ville"] } },
        "TZ": { name: "Tanzanie", flag: "🇹🇿", dialCode: "+255", phonePlaceholder: "750 000 000", phoneLength: 9, defaultCity: "Dar es Salaam", cities: { "Dar es Salaam": ["Kinondoni (Masaki, Oysterbay)", "Ilala (CBD)", "Temeke", "Ubungo", "Kigamboni"], "Zanzibar": ["Stone Town", "Nungwi", "Paje"], "Autres villes": ["Arusha", "Dodoma", "Mwanza", "Moshi", "Mbeya", "Autre ville"] } }
    };

    // Attribution globale pour compatibilité ascendante et transverse
    window.AZORIA_COUNTRIES = COUNTRIES;
    window.WEST_AFRICA_LOCATIONS = COUNTRIES;

    /**
     * Retourne la liste complète de tous les pays, avec priorité pour les marchés clés
     */
    window.getAllCountriesList = function () {
        return Object.keys(COUNTRIES).map(code => ({
            code: code,
            name: COUNTRIES[code].name,
            flag: COUNTRIES[code].flag,
            dialCode: COUNTRIES[code].dialCode,
            phonePlaceholder: COUNTRIES[code].phonePlaceholder,
            phoneLength: COUNTRIES[code].phoneLength,
            defaultCity: COUNTRIES[code].defaultCity,
            cities: COUNTRIES[code].cities
        }));
    };

    /**
     * Recherche d'un pays par son code ISO (CI, SN, FR...)
     */
    window.getCountryByCode = function (code) {
        if (!code) return COUNTRIES['CI'];
        const normalized = code.toUpperCase().trim();
        return COUNTRIES[normalized] || COUNTRIES['CI'];
    };

    /**
     * Helper Alpine.js pour générer l'état de dropdown dépendant (Pays -> Ville -> Commune/Quartier)
     */
    window.createLocationSelector = function (initialCountry = 'CI', initialCity = null, initialZone = null) {
        return {
            selectedCountry: (initialCountry in COUNTRIES) ? initialCountry : 'CI',
            selectedCity: initialCity,
            selectedZone: initialZone,
            allCountries: window.getAllCountriesList(),

            initLocation() {
                const countryData = COUNTRIES[this.selectedCountry] || COUNTRIES['CI'];
                if (!this.selectedCity || !(this.selectedCity in countryData.cities)) {
                    this.selectedCity = countryData.defaultCity || Object.keys(countryData.cities)[0];
                }
                const zones = countryData.cities[this.selectedCity] || [];
                if (!this.selectedZone || !zones.includes(this.selectedZone)) {
                    this.selectedZone = zones[0] || '';
                }
            },

            get currentCountry() {
                return COUNTRIES[this.selectedCountry] || COUNTRIES['CI'];
            },

            get availableCities() {
                return Object.keys(this.currentCountry.cities || {});
            },

            get availableZones() {
                return (this.currentCountry.cities && this.currentCountry.cities[this.selectedCity]) ? this.currentCountry.cities[this.selectedCity] : [];
            },

            onCountryChange() {
                const countryData = this.currentCountry;
                this.selectedCity = countryData.defaultCity || (countryData.cities ? Object.keys(countryData.cities)[0] : 'Centre-ville');
                const zones = (countryData.cities && countryData.cities[this.selectedCity]) ? countryData.cities[this.selectedCity] : [];
                this.selectedZone = zones[0] || '';
            },

            onCityChange() {
                const zones = this.availableZones;
                this.selectedZone = zones[0] || '';
            },

            get fullLocationString() {
                return `${this.selectedZone ? this.selectedZone + ', ' : ''}${this.selectedCity} (${this.currentCountry.name})`;
            }
        };
    };
})();
