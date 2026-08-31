/**
 * Azoria - Base de données géographique & sélecteur dépendant pour l'Afrique de l'Ouest
 * Pays supportés : Côte d'Ivoire 🇨🇮, Sénégal 🇸🇳, Mali 🇲🇱, Burkina Faso 🇧🇫, Bénin 🇧🇯, Togo 🇹🇬, Guinée 🇬🇳, Niger 🇳🇪
 */

window.WEST_AFRICA_LOCATIONS = {
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
            "Bouaké": [
                "Koko", "Nimbo", "Belleville", "Air France", "N'gattakro", "Broukro", "Commerce", "Ahougnanssou", "Autre quartier"
            ],
            "Yamoussoukro": [
                "Morofé", "Assabou", "220 Logements", "Kokrenou", "Habitat", "Fondation", "N'zuessy", "Autre quartier"
            ],
            "San-Pédro": [
                "Bardot", "Cité", "Séwéké", "Balmer", "Lac", "Zone Industrielle", "Autre quartier"
            ],
            "Korhogo": [
                "Koko", "Petit Paris", "Sinistré", "Tchékélé", "Soba", "Kassirimé", "Autre quartier"
            ],
            "Daloa": [
                "Tazibouo", "Lobia", "Marais", "Gbeuliville", "Commerce", "Autre quartier"
            ],
            "Man": [
                "Grand Gbapleu", "Koko", "Domoraud", "Doyagouiné", "Sari", "Autre quartier"
            ],
            "Grand-Bassam": [
                "Quartier France", "Moossou", "Impérial", "Rosiers", "Phare", "Autre quartier"
            ],
            "Autres villes (Intérieur)": [
                "Soubré", "Gagnoa", "Abengourou", "Bondoukou", "Divo", "Agboville", "Ferkessédougou", "Adzopé", "Autre commune"
            ]
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
            "Dakar": [
                "Dakar Plateau", "Almadies / Ngor", "Ouakam / Mamelles", "Mermoz / Sacré-Cœur",
                "Fann / Point E", "Médina / Gueule Tapée", "Yoff / Nord Foire",
                "Grand Yoff / Liberté", "Parcelles Assainies", "Pikine", "Guédiawaye", "Rufisque / Diamniadio"
            ],
            "Thiès": [
                "Grand Thiès", "Mbour 1 / 2", "Randoulène", "Dixième", "Cité Lamy", "Autre quartier"
            ],
            "Saint-Louis": [
                "Île de Saint-Louis", "Sor", "Balacoss", "Ndar Toute", "Pikine", "Autre quartier"
            ],
            "Mbour / Saly": [
                "Saly Portudal", "Somone", "Ngaparou", "Grand Mbour", "Tefess", "Autre quartier"
            ],
            "Touba / Mbacké": [
                "Touba Mosquée", "Darou Marnane", "Mbacké Centre", "Gouye Mbinde", "Autre quartier"
            ],
            "Ziguinchor": [
                "Boucotte", "Santhiaba", "Lyndiane", "Kenia", "Autre quartier"
            ],
            "Autres villes du Sénégal": [
                "Kaolack", "Kolda", "Tambacounda", "Louga", "Fatick", "Kédougou", "Autre localité"
            ]
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
            "Bamako": [
                "Commune I (Korofina, Banconi, Fadjiguila)",
                "Commune II (Hippodrome, Médina-Coura, Bozola)",
                "Commune III (Badiallan, Centre Commercial, Darsalam)",
                "Commune IV (Hamdallaye, Lafiabougou, ACI 2000, Djicoroni)",
                "Commune V (Badalabougou, Baco Djicoroni, Torokorobougou, Quartier Mali)",
                "Commune VI (Sogoniko, Yirimadio, Faladié, Missabougou, Magnambougou)"
            ],
            "Sikasso": [
                "Wayerma", "Mancourani", "Mamelon", "Bougoula", "Autre quartier"
            ],
            "Ségou": [
                "Ségou Koro", "Angoulême", "Pelengana", "Médine", "Autre quartier"
            ],
            "Kayes": [
                "Kayes N'Di", "Légal Ségou", "Khasso", "Liberté", "Autre quartier"
            ],
            "Autres villes du Mali": [
                "Mopti", "Koulikoro", "Gao", "Koutiala", "San", "Autre localité"
            ]
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
            "Ouagadougou": [
                "Ouaga 2000", "Koulouba / Centre-ville", "Gounghin", "Pissy",
                "Patte d'Oie", "Dassasgho", "Karpala", "Tampouy", "Saaba", "Somgandé"
            ],
            "Bobo-Dioulasso": [
                "Bindougousso", "Sarfalao", "Koko", "Accart-ville", "Colma", "Lafiabougou", "Autre quartier"
            ],
            "Koudougou": [
                "Secteur 1", "Secteur 2", "Palogo", "Burkindi", "Autre quartier"
            ],
            "Autres villes du Burkina": [
                "Banfora", "Ouahigouya", "Fada N'Gourma", "Dédougou", "Kaya", "Autre localité"
            ]
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
            "Cotonou": [
                "Cadjèhoun / Haie Vive", "Akpakpa (Dodomè, PK6, Senadé)", "Gbégamey / Saint-Michel",
                "Fidjrossè / Plage", "Ménontin / Zogbo", "Kouhounou / Stade", "Vodjè / Maro-Militaire"
            ],
            "Abomey-Calavi": [
                "Godomey / Togoudo", "Arconville", "Calavi Centre", "Tankpè", "Akassato", "Zinvié"
            ],
            "Porto-Novo": [
                "Ouando", "Avakpa", "Djassin", "Attakè", "Dowa", "Autre quartier"
            ],
            "Parakou": [
                "Albarika", "Camp Adagbè", "Zongo", "Banikanni", "Autre quartier"
            ],
            "Autres villes du Bénin": [
                "Ouidah", "Bohicon", "Abomey", "Natitingou", "Djougou", "Autre localité"
            ]
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
            "Lomé": [
                "Tokoin (Forever, Gbadago, Wuiti, Casablanca)", "Bè (Kpota, Beach, Adidomé)",
                "Nyékonakpoè / Kodjoviakopé", "Agoè-Nyivé (Assiyéyé, Téléphone, Minamadou)",
                "Hédzranawoé / Aéroport", "Baguida / Avépozo", "Adidogomé / Zossimé", "Kégué / Stade"
            ],
            "Kara": [
                "Lama", "Chaminade", "Kpédah", "Tchintchinda", "Autre quartier"
            ],
            "Sokodé": [
                "Didaouré", "Kparatao", "Komah", "Tchaoudjo", "Autre quartier"
            ],
            "Kpalimé": [
                "Kpodzi", "Zomayi", "Nyivémé", "Kuma", "Autre quartier"
            ],
            "Autres villes du Togo": [
                "Atakpamé", "Dapaong", "Tsévié", "Aného", "Autre localité"
            ]
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
            "Conakry": [
                "Kaloum (Centre-ville, Almamya, Boulbinet)",
                "Dixinn (Minière, Camayenne, Hafia, Belle-vue)",
                "Matam (Madina, Bonfi, Touguiwondy, Carrière)",
                "Ratoma (Kipé, Nongo, Lambanyi, Taouyah, Cosa, Bambéto)",
                "Matoto (Yimbaya, Entag, Dabompa, Gbessia, Sangoyah)"
            ],
            "Kindia": [
                "Tafory", "Manquepas", "Caravansérail", "Féréfou", "Autre quartier"
            ],
            "Kankan": [
                "Bordo", "Missira", "Kabada", "Dibida", "Autre quartier"
            ],
            "Labé": [
                "Pounthioun", "Daka", "Mosquée", "Kouroula", "Autre quartier"
            ],
            "Autres villes de Guinée": [
                "Nzérékoré", "Mamou", "Boké", "Faranah", "Kamsar", "Autre localité"
            ]
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
            "Niamey": [
                "Niamey I (Plateau, Yantala, Goudel)",
                "Niamey II (Boukoki, Lazaret, Talladjé)",
                "Niamey III (Koira Kano, Dar-Es-Salam, Recasement)",
                "Niamey IV (Gamkalley, Saga, Aéroport)",
                "Niamey V (Harobanda, Rive Droite, Karadjé)"
            ],
            "Maradi": [
                "Ali Dan Sofo", "Zaria", "Bagalam", "Maradi Centre", "Autre quartier"
            ],
            "Zinder": [
                "Birni", "Zengou", "Garin Malam", "Sabal", "Autre quartier"
            ],
            "Autres villes du Niger": [
                "Tahoua", "Agadez", "Dosso", "Diffa", "Tillabéri", "Autre localité"
            ]
        }
    }
};

/**
 * Helper Alpine.js pour générer l'état de dropdown dépendant (Pays -> Ville -> Commune/Quartier)
 */
window.createLocationSelector = function (initialCountry = 'CI', initialCity = null, initialZone = null) {
    return {
        selectedCountry: initialCountry in window.WEST_AFRICA_LOCATIONS ? initialCountry : 'CI',
        selectedCity: initialCity,
        selectedZone: initialZone,

        initLocation() {
            const countryData = window.WEST_AFRICA_LOCATIONS[this.selectedCountry];
            if (!this.selectedCity || !(this.selectedCity in countryData.cities)) {
                this.selectedCity = countryData.defaultCity || Object.keys(countryData.cities)[0];
            }
            const zones = countryData.cities[this.selectedCity] || [];
            if (!this.selectedZone || !zones.includes(this.selectedZone)) {
                this.selectedZone = zones[0] || '';
            }
        },

        get currentCountry() {
            return window.WEST_AFRICA_LOCATIONS[this.selectedCountry] || window.WEST_AFRICA_LOCATIONS['CI'];
        },

        get availableCities() {
            return Object.keys(this.currentCountry.cities);
        },

        get availableZones() {
            return this.currentCountry.cities[this.selectedCity] || [];
        },

        onCountryChange() {
            const countryData = this.currentCountry;
            this.selectedCity = countryData.defaultCity || Object.keys(countryData.cities)[0];
            const zones = countryData.cities[this.selectedCity] || [];
            this.selectedZone = zones[0] || '';
        },

        onCityChange() {
            const zones = this.availableZones;
            this.selectedZone = zones[0] || '';
        },

        get fullLocationString() {
            return `${this.selectedZone}, ${this.selectedCity} (${this.currentCountry.name})`;
        }
    };
};
