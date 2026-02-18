// Araç segmentleri ve marka/model/tür eşleştirmesi
export const ARAÇ_SEGMENT_LISTESI = [
    { segment: "düşük", markalar: ["Tofaş", "Lada", "Proton"] },
    { segment: "orta", markalar: ["Fiat", "Renault", "Hyundai", "Dacia", "Opel", "Peugeot", "Citroen", "Ford", "Volkswagen", "Skoda", "Seat", "Kia", "Suzuki", "Mazda", "Mitsubishi", "Chery", "MG", "Isuzu", "SsangYong (KGM)", "Geely"] },
    { segment: "lüks", markalar: ["Mercedes-Benz", "BMW", "Audi", "Porsche", "Tesla", "Jaguar", "Land Rover", "Lexus", "Infiniti", "Maserati", "Ferrari", "Lamborghini", "Bentley", "Rolls-Royce", "Aston Martin", "Alpine", "Lotus"] },
    { segment: "ticari", modeller: ["Doblo", "Fiorino", "Transit", "Transporter", "Sprinter", "Jumpy", "Boxer", "Vivaro", "Caddy", "Kangoo", "Ducato", "Master", "Daily", "Bongo", "e-Deliver", "Mifa", "Atak", "Jest", "e-Jest", "e-ATA", "Proace", "Hiace", "Crafter", "Amarok", "Constellation", "Delivery", "e-Delivery", "Volksbus", "TGE", "TGL", "TGM", "TGS", "TGX", "Lion's Coach", "Lion's City", "Tourliner", "Cityliner", "Sultan", "Kent", "e-Kent", "e-Territo", "Ulyso", "Cobra", "Akrep", "Arma", "Tuğra", "Procity", "Neocity", "Neoport", "Apron", "Kirpi", "Vuran", "Amazon", "Altuğ", "Tulga"] },
    { segment: "minibüs", modeller: ["Minibüs", "Ducato Minibüs", "Master Minibüs", "Sprinter Minibüs", "Jumper Minibüs", "Boxer Minibüs", "MD9", "MD9 electriCITY", "TS 45", "Sultan", "Kent", "e-Kent", "e-Territo", "Ulyso", "Jest", "e-Jest", "Atak", "e-Atak", "Otonom e-Atak", "Star", "e-ATA", "e-ATA Hydrogen", "Mifa", "e-Deliver", "Daily Minibüs"] },
    { segment: "otobüs", modeller: ["Otobüs", "Travego", "Tourismo", "Intouro", "Conecto", "Citaro", "CapaCity", "eCitaro", "eCitaro G", "Lion's Coach", "Lion's City", "Tourliner", "Cityliner", "Sultan", "Kent", "e-Kent", "e-Territo", "Ulyso", "Cobra", "Akrep", "Arma", "MD9", "MD9 electriCITY", "TS 45"] },
    { segment: "kamyonet", modeller: ["Kamyonet", "Ducato Kamyonet", "Master Kamyonet", "Sprinter Kamyonet", "Jumper Kamyonet", "Boxer Kamyonet", "Vivaro Kamyonet", "Daily Şasi Kamyonet", "Crafter Kamyonet", "Amarok", "Constellation", "Delivery", "e-Delivery", "Volksbus", "TGE", "TGL", "TGM", "TGS", "TGX"] }
];

// Araç segmentini bulmak için yardımcı fonksiyon (frontendde kullanılabilir)
export function getAracSegment(marka, model, arac_turu) {
    // Önce model bazlı segment eşleşmesi
    for (const seg of ARAÇ_SEGMENT_LISTESI) {
        if (seg.modeller && seg.modeller.some(m => model && model.toLowerCase().includes(m.toLowerCase()))) {
            return seg.segment;
        }
    }
    // Sonra marka bazlı segment eşleşmesi
    for (const seg of ARAÇ_SEGMENT_LISTESI) {
        if (seg.markalar && seg.markalar.some(m => marka && marka.toLowerCase() === m.toLowerCase())) {
            return seg.segment;
        }
    }
    // Araç türü bazlı (ör: Motosiklet, Otobüs, Minibüs, Kamyonet)
    if (arac_turu) {
        const t = arac_turu.toLowerCase();
        if (t.includes("kamyonet")) return "kamyonet";
        if (t.includes("minibüs")) return "minibüs";
        if (t.includes("otobüs")) return "otobüs";
        if (t.includes("ticari")) return "ticari";
    }
    return "orta"; // default
}
// Otomobil markaları (kısaltmalar açıldı, popülerler eklendi)
export const MARKA_LISTESI = [
    "Volkswagen",
    "Renault",
    "Fiat",
    "Ford",
    "Hyundai",
    "Toyota",
    "Peugeot",
    "Opel",
    "Citroen",
    "Honda",
    "Dacia",
    "Nissan",
    "Seat",
    "Skoda",
    "Kia",
    "Mercedes-Benz",
    "BMW",
    "Audi",
    "Chevrolet",
    "Suzuki",
    "Mazda",
    "Mitsubishi",
    "Volvo",
    "MINI", // Mini -> MINI (uyumlu olması için)
    "Jeep",
    "Land Rover",
    "Porsche",
    "Tesla",
    "Subaru",
    "Alfa Romeo",
    "Lexus",
    "Chery",
    "MG",
    "Cupra",
    "Smart",
    "Isuzu",
    "SsangYong (KGM)", // SsangYong -> SsangYong (KGM)
    "Infiniti",
    "Jaguar",
    "Saab",
    "Proton",
    "Geely",
    "Togg",
    // Eksik olanlar eklendi:
    "BYD",
    "Maserati",
    "Ferrari",
    "Lamborghini",
    "Aston Martin",
    "Bentley",
    "Rolls-Royce",
    "Otokar",
    "TEMSA",
    "MAN",
    "Skywell",
    "Leapmotor",
    "Seres / DFSK",
    "Voyah",
    "Hongqi",
    "Maxus",
    "Alpine",
    "Lotus",
    "Arora",
    "BMC",
    "DS Automobiles",
    "Iveco",
    "Karsan",
    "Lada",
    "Range Rover", // Range Rover ayrı marka olarak da ekleniyor
    "Tofaş"
];


// Model listesi: marka-model eşleşmesi, sadeleştirilmiş
export const MODEL_LISTESI = [
    // Mercedes-Benz
    ...["A-Serisi Hatchback","A-Serisi Sedan","B-Serisi","C-Serisi Sedan","C-Serisi Estate","C-Serisi All-Terrain","CLA Coupé","CLA Shooting Brake","CLE Coupé","CLE Cabriolet","E-Serisi Sedan","E-Serisi Estate","E-Serisi All-Terrain","EQA","EQB","EQE Sedan","EQE SUV","EQS Sedan","EQS SUV","G-Serisi","GLA","GLB","GLC SUV","GLC Coupé","GLE SUV","GLE Coupé","GLS","S-Serisi Sedan","Mercedes-Maybach S-Serisi","Mercedes-Maybach GLS","Mercedes-Maybach EQS SUV","Mercedes-AMG GT Coupé","Mercedes-AMG GT 4-Kapı Coupé","Mercedes-AMG SL Roadster","Citan Panelvan","Citan Tourer","T-Serisi","Vito Panelvan","Vito Tourer","Vito Mixto","eVito Panelvan","eVito Tourer","V-Serisi","EQV","Sprinter Panelvan","Sprinter Tourer","Sprinter Kamyonet","eSprinter","Travego","Tourismo","Intouro","Conecto","Citaro","Citaro K","Citaro G","CapaCity","eCitaro","eCitaro G","Actros","Actros L","Arocs","Atego","Econic","Unimog","Zetros","eActros 300/400","eActros 600","eEconic"].map(model=>({marka:"Mercedes-Benz",model})),
    // Tesla
    ...["Model Y","Model 3","Model S","Model X","Cybertruck"].map(model=>({marka:"Tesla",model})),
    // Porsche
    ...["911 Carrera","911 Turbo","911 GT3","718 Cayman","718 Boxster","Taycan","Taycan Cross Turismo","Panamera","Panamera Sport Turismo","Macan","Macan Elektrik","Cayenne","Cayenne Coupé"].map(model=>({marka:"Porsche",model})),
    // BYD
    ...["Atto 3","Seal U DM-i","Han","Tang","Dolphin","Seal"].map(model=>({marka:"BYD",model})),
    // Maserati
    ...["Grecale","Levante","Ghibli","Quattroporte","MC20","MC20 Cielo","GranTurismo"].map(model=>({marka:"Maserati",model})),
    // Ferrari
    ...["Roma","Roma Spider","296 GTB","296 GTS","SF90 Stradale","SF90 Spider","812 Superfast","812 GTS","Purosangue","Daytona SP3","12Cilindri"].map(model=>({marka:"Ferrari",model})),
    // Lamborghini
    ...["Huracán","Revuelto","Urus","Urus S","Urus Performante","Temerario"].map(model=>({marka:"Lamborghini",model})),
    // Aston Martin
    ...["Vantage","DB12","DBX","DBX707","DBS","Valhalla"].map(model=>({marka:"Aston Martin",model})),
    // Bentley
    ...["Continental GT","Continental GTC","Flying Spur","Bentayga","Bentayga EWB"].map(model=>({marka:"Bentley",model})),
    // Rolls-Royce
    ...["Phantom","Ghost","Cullinan","Spectre","Black Badge Serisi"].map(model=>({marka:"Rolls-Royce",model})),
    // Otokar
    ...["Atlas (Kamyon)","Sultan (Minibüs/Otobüs)","Sultan Comfort","Sultan Mega","Sultan Giga","Doruk","Kent","Kent Körüklü","e-Kent","e-Territo","Ulyso","Cobra II","Akrep II","Arma"].map(model=>({marka:"Otokar",model})),
    // TEMSA
    ...["Prestij SX","Safir Plus","Maraton","Avenue","Avenue Electron","Avenue EV","MD9","MD9 electriCITY","TS 45"].map(model=>({marka:"TEMSA",model})),
    // MAN
    ...["TGE (Panelvan/Minibüs)","TGL","TGM","TGS","TGX (Çekici/Kamyon)","Lion's Coach (Otobüs)","Lion's City","Neoplan Tourliner","Neoplan Cityliner"].map(model=>({marka:"MAN",model})),
    // Skywell
    ...["ET5","ET5 LR"].map(model=>({marka:"Skywell",model})),
    // Leapmotor
    ...["T03","C10"].map(model=>({marka:"Leapmotor",model})),
    // Seres / DFSK
    ...["Seres 3","E5","Fengon 5","Fengon 500","K01","C31","C32"].map(model=>({marka:"Seres / DFSK",model})),
    // Voyah
    ...["Free"].map(model=>({marka:"Voyah",model})),
    // Hongqi
    ...["E-HS9"].map(model=>({marka:"Hongqi",model})),
    // Maxus
    ...["e-Deliver 3","e-Deliver 9","Mifa 9"].map(model=>({marka:"Maxus",model})),
    // Alpine
    ...["A110","A110 GT","A110 S","A290"].map(model=>({marka:"Alpine",model})),
    // Lotus
    ...["Emira","Eletre","Emeya"].map(model=>({marka:"Lotus",model})),
    // Genel araç türleri (modelsiz)
    { marka: "Motosiklet", model: "" },
    { marka: "Otobüs", model: "" },
    { marka: "Traktör", model: "" },
    { marka: "Vinç", model: "" },
    { marka: "Minibüs", model: "" },
    { marka: "Kamyon", model: "" },
    { marka: "Kamyonet", model: "" },
    { marka: "Çekici", model: "" },
    // BMW
    ...["1 Serisi","2 Serisi Coupé","2 Serisi Gran Coupé","2 Serisi Active Tourer","3 Serisi Sedan","3 Serisi Touring","4 Serisi Coupé","4 Serisi Cabriolet","4 Serisi Gran Coupé","5 Serisi Sedan","5 Serisi Touring","7 Serisi Sedan","8 Serisi Coupé","8 Serisi Cabriolet","8 Serisi Gran Coupé","Z4 Roadster","X1","X2","X3","X4","X5","X6","X7","XM","iX1","iX2","iX3","iX","i4","i5 Sedan","i5 Touring","i7","M2 Coupé","M3 Sedan","M3 Touring","M4 Coupé","M4 Cabriolet","M5 Sedan","M8 Coupé","M8 Cabriolet","M8 Gran Coupé","X3 M","X4 M","X5 M","X6 M","G 310 R","G 310 GS","C 400 X","C 400 GT","CE 02","CE 04","F 800 GS","F 900 GS","F 900 GS Adventure","F 900 R","F 900 XR","R 12","R 12 nineT","R 1250 GS Adventure","R 1250 RT","R 1250 R","R 1250 RS","R 1300 GS","R 1300 GS Adventure","S 1000 R","S 1000 RR","S 1000 XR","M 1000 R","M 1000 RR","M 1000 XR","K 1600 GT","K 1600 GTL","K 1600 B","K 1600 Grand America","R 18","R 18 Classic","R 18 B","R 18 Roctane","R 18 Transcontinental"].map(model=>({marka:"BMW",model})),
    // Volkswagen
    ...["Polo","Golf","Golf Variant","T-Cross","Taigo","T-Roc","Tiguan","Tiguan Allspace","Touareg","Passat Variant","ID.3","ID.4","ID.5","ID.7","ID. Buzz","Caddy","Caddy Cargo","Caddy Exclusive","Transporter Panelvan","Transporter City Van","Caravelle","Multivan","California","Crafter Panelvan","Crafter Servis","Crafter Okul","Crafter Kamyonet","Amarok","Meteor","Constellation","Delivery","e-Delivery","Volksbus"].map(model=>({marka:"Volkswagen",model})),
    // Renault
    ...["Clio","Taliant","Captur","Megane Sedan","Megane E-Tech","Austral","Arkana","Rafale","Espace","Symbioz","Renault 5 E-Tech","Renault Duster","Kangoo Multix","Kangoo Van","Express Van","Express Combi","Trafic Panelvan","Trafic Multix","Trafic Combi","Master Panelvan","Master Kamyonet","Master Minibüs","Master Citybus","T Serisi","T High Serisi","C Serisi","K Serisi","D Serisi","D Wide Serisi","E-Tech T/C/D"].map(model=>({marka:"Renault",model})),
    // Fiat
    ...["Panda","Panda City Cross","500","500e","500X","600","600e","Topolino","Egea Sedan","Egea Hatchback","Egea Cross","Egea Cross Wagon","Fiorino Combi","Fiorino Cargo","Doblo Combi","Doblo Cargo","Scudo","Ducato Van","Ducato Kamyonet","Ducato Minibüs","Ulysse","E-Ducato","E-Scudo","E-Doblo","Pratico"].map(model=>({marka:"Fiat",model})),
    // Alfa Romeo
    ...["Junior","Tonale","Giulia","Stelvio","33 Stradale"].map(model=>({marka:"Alfa Romeo",model})),
    // Arora
    ...["Cappucino 50","Cappucino 125","Mojito","Vesta 50","Verano 50","Beatrix","Max-T","Safari 50","Safari 125","Freedom 50","Derya 50","Derya 125","AR 125-2","AR 250","GT 250","GS 250","ZRX 200","Kasırga","MT 125","Yeni T-5","ARS 200","XMAX","Adventure","Sorrento","Q5","Q3","Dream","Panther","Tiger","Lion","Alfa","Ata","Triar"].map(model=>({marka:"Arora",model})),
    // Audi
    ...["A1 Sportback","A3 Sedan","A3 Sportback","S3 Sedan","S3 Sportback","RS 3 Sedan","RS 3 Sportback","A4 Sedan","A4 Avant","A4 allroad quattro","S4 Sedan","S4 Avant","RS 4 Avant","A5 Coupé","A5 Sportback","A5 Cabriolet","S5 Coupé","S5 Sportback","S5 Cabriolet","RS 5 Coupé","RS 5 Sportback","A6 Sedan","A6 Avant","A6 allroad quattro","S6 Sedan","S6 Avant","RS 6 Avant","RS 6 Avant GT","A7 Sportback","S7 Sportback","RS 7 Sportback","A8","A8 L","S8","Q2","SQ2","Q3","Q3 Sportback","RS Q3","RS Q3 Sportback","Q4 e-tron","Q4 Sportback e-tron","Q5","Q5 Sportback","SQ5","SQ5 Sportback","Q6 e-tron","SQ6 e-tron","Q7","SQ7","Q8","SQ8","RS Q8","Q8 e-tron","Q8 Sportback e-tron","SQ8 e-tron","SQ8 Sportback e-tron","e-tron GT quattro","RS e-tron GT"].map(model=>({marka:"Audi",model})),
    // BMC
    ...["Tuğra T Serisi","Tuğra K Serisi","Tuğra D Serisi","Procity 12m Dizel","Procity 12m CNG","Procity 18m Dizel","Procity 18m CNG","Procity Tech 12m Elektrikli","Neocity 8.5m Dizel","Neocity 8.5m Elektrikli","Neocity 10m Dizel","Neoport","Apron","Kirpi II","Vuran","Amazon","Altuğ 8x8","Tulga"].map(model=>({marka:"BMC",model})),
    // Chery
    ...["Omoda 5","Omoda 5 Pro","Tiggo 4 Pro","Tiggo 7 Pro","Tiggo 7 Pro Max","Tiggo 8 Pro","Tiggo 8 Pro Max","Tiggo 8 Pro Plug-in Hybrid","Arrizo 8","eQ1","eQ7"].map(model=>({marka:"Chery",model})),
    // Chevrolet
    ...["Spark","Malibu","Camaro","Corvette Stingray","Corvette Z06","Corvette E-Ray","Trax","Trailblazer","Equinox","Equinox EV","Blazer","Blazer EV","Traverse","Tahoe","Suburban","Colorado","Silverado 1500","Silverado HD","Silverado EV","Express Cargo Van","Express Passenger Van"].map(model=>({marka:"Chevrolet",model})),
    // Citroën
    ...["Ami","C3","C3 Aircross","C4","C4 X","ë-C4","ë-C4 X","C5 Aircross","C5 X","Berlingo","Berlingo Van","Jumpy Panelvan","Jumpy Spacetourer","Jumper Panelvan","Jumper Minibüs","Jumper Kamyonet"].map(model=>({marka:"Citroën",model})),
    // Chrysler
    ...["Pacifica","Pacifica Plug-in Hybrid","Voyager","300"].map(model=>({marka:"Chrysler",model})),
    // Cupra
    ...["Leon","Leon Sportstourer","Ateca","Formentor","Born","Tavascan","Terramar","DarkRebel","Raval"].map(model=>({marka:"Cupra",model})),
    // Dacia
    ...["Spring","Sandero","Sandero Stepway","Duster","Yeni Duster","Jogger","Logan"].map(model=>({marka:"Dacia",model})),
    // DS Automobiles
    ...["DS 3","DS 4","DS 7","DS 9"].map(model=>({marka:"DS Automobiles",model})),
    // Ford
    ...["Fiesta","Focus","Puma","Kuga","Mustang","Mustang Mach-E","Explorer Elektrikli","Explorer SUV","Bronco","Territory","Tourneo Courier","Transit Courier","Tourneo Connect","Transit Connect","Tourneo Custom","Transit Custom","Transit Van","Transit Kamyonet","Transit Minibüs","Ranger","Ranger Raptor","Maverick","F-150","F-150 Lightning","F-MAX","F-Line Çekici","F-Line Yol Kamyonu","F-Line İnşaat Kamyonu","Cargo"].map(model=>({marka:"Ford",model})),
    // Honda
    ...["Jazz e:HEV","City","Civic Sedan","Civic Type R","HR-V e:HEV","ZR-V e:HEV","CR-V e:HEV","PCX125","Dio","Activa 125","Forza 250","Forza 750","X-ADV","Africa Twin","NC750X","Transalp","Gold Wing","CBR Serisi"].map(model=>({marka:"Honda",model})),
    // Hyundai
    ...["i10","i20","i20 N","i30","Bayon","Kona","Kona Elektrik","Tucson","Santa Fe","Ioniq 5","Ioniq 6","Staria","H-100"].map(model=>({marka:"Hyundai",model})),
    // Isuzu
    ...["D-Max","NPR","N-Wide","N-Long","Grand Toro","Novo","Novo Lux","Turquoise","Visigo","Kendo / Interliner","Citiport 12","Citiport 18","Novociti Life","Novociti Volt","Big.e"].map(model=>({marka:"Isuzu",model})),
    // Iveco
    ...["Daily Panelvan","Daily Şasi Kamyonet","Daily 4x4","Daily Minibüs","Eurocargo","S-Way","T-Way","X-Way"].map(model=>({marka:"Iveco",model})),
    // Jeep
    ...["Avenger","Renegade","Compass","Wrangler","Grand Cherokee"].map(model=>({marka:"Jeep",model})),
    // Karsan
    ...["Jest+","e-Jest","Atak","e-Atak","Otonom e-Atak","Star","e-ATA 10m","e-ATA 12m","e-ATA 18m","e-ATA Hydrogen"].map(model=>({marka:"Karsan",model})),
    // Kia
    ...["Picanto","Stonic","Cerato","Ceed Hatchback","Ceed Sportswagon","XCeed","Niro EV","Sportage","Sorento","EV3","EV6","EV9","Bongo"].map(model=>({marka:"Kia",model})),
    // Mazda
    ...["Mazda2","Mazda2 Hybrid","Mazda3 Hatchback","Mazda3 Sedan","Mazda6 Sedan","Mazda6 Wagon","CX-3","CX-30","CX-5","CX-50","CX-60","CX-70","CX-80","CX-90","MX-30","MX-5","MX-5 RF","BT-50"].map(model=>({marka:"Mazda",model})),
    // Land Rover
    ...["Range Rover","Range Rover Sport","Range Rover Velar","Range Rover Evoque","Discovery","Discovery Sport","Defender 90","Defender 110","Defender 130","Defender Octa"].map(model=>({marka:"Land Rover",model})),
    // Lada
    ...["Granta Sedan","Granta Liftback","Granta Hatchback","Granta Cross","Granta Sport","Vesta Sedan","Vesta Cross","Vesta SW","Vesta SW Cross","Vesta Sportline","Niva Legend","Niva Bronto","Niva Travel","Largus Universal","Largus Cross","Largus Panelvan"].map(model=>({marka:"Lada",model})),
    // MG
    ...["MG3","MG3 Hybrid+","MG4 Electric","MG5 Electric","MG ZS","MG ZS EV","MG HS","MG EHS","MG One","MG GT","MG7","Marvel R Electric","Cyberster","Hector","Gloster"].map(model=>({marka:"MG",model})),
    // MINI
    ...["Cooper 3 Kapı","Cooper 5 Kapı","Cooper Cabrio","Cooper S","Cooper SE","Aceman","Countryman","Countryman S","Countryman SE","John Cooper Works"].map(model=>({marka:"MINI",model})),
    // Mitsubishi
    ...["Space Star","Colt","ASX","Eclipse Cross","Outlander","Outlander PHEV","Xforce","Pajero Sport","L200"].map(model=>({marka:"Mitsubishi",model})),
    // Nissan
    ...["Micra","Juke","Qashqai","Qashqai e-Power","X-Trail","Ariya","Leaf","Z","GT-R","Townstar Combi","Townstar Van","Primastar","Interstar","Navara"].map(model=>({marka:"Nissan",model})),
    // Opel
    ...["Corsa","Corsa Elektrik","Astra","Astra Elektrik","Mokka","Mokka Elektrik","Crossland","Frontera","Grandland","Rocks Elektrik","Combo Life","Combo Cargo","Combo Elektrik","Zafira Life","Vivaro Cargo","Vivaro City Van","Vivaro Elektrik","Movano","Movano Elektrik"].map(model=>({marka:"Opel",model})),
    // Peugeot
    ...["208","E-208","308","E-308","408","508","508 PSE","2008","E-2008","3008","E-3008","5008","E-5008","Rifter","Partner Van","Expert Van","Expert Combi","Traveller","Boxer Van","Boxer Minibüs","Landtrek"].map(model=>({marka:"Peugeot",model})),
    // Range Rover (Tekrar)
    ...["Range Rover","Range Rover Sport","Range Rover Velar","Range Rover Evoque"].map(model=>({marka:"Range Rover",model})),
    // Seat
    ...["Ibiza","Leon","Leon Sportstourer","Arona","Ateca","Tarraco","Mó 125","Mó 50"].map(model=>({marka:"Seat",model})),
    // Scania
    ...["L Serisi","P Serisi","G Serisi","R Serisi","S Serisi","V8 Serisi","XT Serisi","Scania Super","Citywide","Interlink","Touring","Fencer"].map(model=>({marka:"Scania",model})),
    // Skoda
    ...["Fabia","Scala","Octavia Sedan","Octavia Combi","Superb Sedan","Superb Combi","Kamiq","Karoq","Kodiaq","Enyaq","Enyaq Coupé","Elroq"].map(model=>({marka:"Skoda",model})),
    // SsangYong (KGM)
    ...["Tivoli","Korando","Torres","Torres EVX","Rexton","Musso Grand"].map(model=>({marka:"SsangYong (KGM)",model})),
    // Subaru
    ...["Solterra","Crosstrek","Forester","Forester e-Boxer","Outback","XV","BRZ","WRX","Impreza","Levorg","Ascent","Legacy"].map(model=>({marka:"Subaru",model})),
    // Suzuki
    ...["Swift","Swift Hibrit","S-Cross Hibrit","Vitara Hibrit","Jimny","Ignis","Swace","Across","Hayabusa","GSX-R1000R","GSX-S1000","GSX-S1000GT","GSX-8S","Katana","V-Strom 1050 DE","V-Strom 800 DE","V-Strom 650 XT","V-Strom 250","SV650","Burgman 400","Burgman 200","Burgman Street 125EX","Address 125","Avenis 125"].map(model=>({marka:"Suzuki",model})),
    // Tofaş
    ...["Murat 124","Murat 131","Serçe","Şahin","Şahin S","Doğan","Doğan L","Doğan SL","Doğan SLX","Kartal","Kartal S","Kartal SLX"].map(model=>({marka:"Tofaş",model})),
    // Toyota
    ...["Corolla Sedan","Corolla Hatchback","Corolla Cross","C-HR","Yaris","Yaris Cross","GR Yaris","RAV4","RAV4 Hybrid","Land Cruiser Prado","Land Cruiser 300","Hilux","Camry","Prius","Mirai","Supra","GR86","Highlander","Aygo X","bZ4X","Proace City","Proace City Cargo","Proace","Proace Verso","Hiace","Coaster"].map(model=>({marka:"Toyota",model})),
    // Togg
    ...["T10X","T10F"].map(model=>({marka:"Togg",model})),
    // Volvo
    ...["S60","S90","V60","V60 Cross Country","V90","V90 Cross Country","XC40","XC60","XC90","C40 Recharge","EX30","EX90","EM90","FH Serisi","FH16","FM Serisi","FMX Serisi","FE Serisi","FL Serisi","Volvo 9900","Volvo 9700","Volvo 8900","Volvo 7900","Volvo BZL"].map(model=>({marka:"Volvo",model})),
    // Lexus
    ...["IS","ES","LS","RC","LC","LBX","UX","NX","RX","RZ","TX","GX","LX","LM"].map(model=>({marka:"Lexus",model})),
    // Smart
    ...["Smart #1","Smart #3","Smart EQ Fortwo","Smart EQ Forfour"].map(model=>({marka:"Smart",model})),
    // Infiniti
    ...["Q50","Q60","QX50","QX55","QX60","QX80"].map(model=>({marka:"Infiniti",model})),
    // Jaguar
    ...["E-PACE","F-PACE","I-PACE","F-TYPE Coupé","F-TYPE Convertible","XE","XF"].map(model=>({marka:"Jaguar",model})),
    // Saab
    ...["Saab 9-3 Sport Sedan","Saab 9-3 Sport Combi","Saab 9-3 Cabriolet","Saab 9-3X","Saab 9-5 Sedan","Saab 9-5 Sport Combi","Saab 9-4X"].map(model=>({marka:"Saab",model})),
    // Proton
    ...["Saga","Iriz","Persona","Exora","S70","X50","X70","X90","e.MAS 7"].map(model=>({marka:"Proton",model})),
    // Geely
    ...["Emgrand","Preface","Coolray","Starray","Okavango","Monjaro","Tugella","Geometry C","Geometry E","Galaxy E8","Galaxy L7","Panda Mini"].map(model=>({marka:"Geely",model})),
];

// Parça adları ve işlem türleri sabitleri

// Parça kodu ve adı ile tam liste (görselden alınan)
export const PARCA_LISTESI_KODLU = [
    { kod: "A.1", ad: "TAVAN SACI" },
    { kod: "A.2", ad: "ÖN PANEL ( SAÇ )" },
    { kod: "A.3", ad: "SAĞ ÖN ÇAMURLUK ( SAÇ )" },
    { kod: "A.4", ad: "SOL ÖN ÇAMURLUK ( SAÇ )" },
    { kod: "A.5", ad: "SAĞ ÖN PODYA SACI" },
    { kod: "A.6", ad: "SOL ÖN PODYA SACI" },
    { kod: "A.7", ad: "SAĞ ŞASİ ÖN" },
    { kod: "A.8", ad: "SOL ŞASİ ÖN" },
    { kod: "A.9", ad: "GÖĞÜS SACI" },
    { kod: "A.10", ad: "MOTOR KAPUTU" },
    { kod: "A.11", ad: "SAĞ ÖN KAPI ( KAPI SACI )" },
    { kod: "A.12", ad: "SOL ÖN KAPI ( KAPI SACI )" },
    { kod: "A.13", ad: "SAĞ ARKA KAPI ( KAPI SACI )" },
    { kod: "A.14", ad: "SOL ARKA KAPI ( KAPI SACI )" },
    { kod: "A.15", ad: "SAĞ MARŞBİYEL ( SAC )" },
    { kod: "A.16", ad: "SOL MARŞBİYEL ( SAC )" },
    { kod: "A.17", ad: "A DİREĞİ SAĞ" },
    { kod: "A.18", ad: "B DİREĞİ SAĞ" },
    { kod: "A.19", ad: "A DİREĞİ SOL" },
    { kod: "A.20", ad: "B DİREĞİ SOL" },
    { kod: "A.21", ad: "BAGAJ KAPAĞI" },
    { kod: "A.22", ad: "ARKA PANEL" },
    { kod: "A.23", ad: "SAĞ ARKA ÇAMURLUK" },
    { kod: "A.24", ad: "SOL ARKA ÇAMURLUK" },
    { kod: "A.25", ad: "HAVUZ SACI" },
    { kod: "A.26", ad: "SAĞ ŞASİ ARKA" },
    { kod: "A.27", ad: "SOL ŞASİ ARKA" },
    { kod: "A.28", ad: "MOTOR TRAVERS / DİNGİL" },
    { kod: "A.29", ad: "YOLCU HAVA YASTIĞI" },
    { kod: "A.30", ad: "SÜRÜCÜ HAVA YASTIĞI" },
    { kod: "A.31", ad: "SAĞ YAN HAVA YASTIĞI" },
    { kod: "A.32", ad: "SOL YAN HAVA YASTIĞI" },
    { kod: "B.1", ad: "MOTOR KAPUTU" },
    { kod: "B.2", ad: "YAN KAPAK ( ADET )" },
    { kod: "B.3", ad: "ANA ŞASİ" },
    { kod: "B.4", ad: "GÖĞÜS SACI" },
    { kod: "B.5", ad: "SAĞ YAN PANEL SACI" },
    { kod: "B.6", ad: "SOL YAN PANEL SACI" },
    { kod: "B.7", ad: "SAĞ ÖN KAPI" },
    { kod: "B.8", ad: "SAĞ ARKA KAPI" },
    { kod: "B.9", ad: "SIRT SACI" },
    { kod: "B.10", ad: "ÇAMURLUK ( SAÇ )" },
    { kod: "B.11", ad: "TABAN SACI ( ADET )" },
    { kod: "B.12", ad: "TAVAN SACI ( ADET )" },
    { kod: "B.13", ad: "ÖN İSKELET" },
    { kod: "B.14", ad: "ARKA İSTEKELET" },
    { kod: "B.15", ad: "YAN İSKELET" },
    { kod: "C.1", ad: "ANA ŞASİ" },
    { kod: "C.2", ad: "MOTOR KAPUTU METAL" },
    { kod: "C.3", ad: "GÖĞÜS SACI" },
    { kod: "C.4", ad: "SOL ÖN DİREK SACI" },
    { kod: "C.5", ad: "SAĞ ÖN DİREK SACI" },
    { kod: "C.6", ad: "TAVAN SACI" },
    { kod: "C.7", ad: "SAĞ YAN PANEL" },
    { kod: "C.8", ad: "SOL YAN PANEL" },
    { kod: "C.9", ad: "SAĞ ÖN KAPI" },
    { kod: "C.10", ad: "SOL ÖN KAPI" },
    { kod: "C.11", ad: "SIRT SACI" },
    { kod: "C.12", ad: "KABİN" },
    { kod: "C.13", ad: "TÜNEL / TABAN SACI" },
    { kod: "D.1", ad: "KABİN" },
    { kod: "D.2", ad: "KAPAK SAC ( ADET )" },
    { kod: "D.3", ad: "MOTOR KAPUTU ( SAC )" },
    { kod: "D.4", ad: "SAĞ ÇAMURLUK ( SAC )" },
    { kod: "D.5", ad: "SOL ÇAMURLUK ( SAC )" },
    { kod: "D.6", ad: "ŞASİ" },
    { kod: "E.1", ad: "TAVAN" },
    { kod: "E.2", ad: "ŞASİ" },
    { kod: "E.3", ad: "SAĞ YAN PANEL" },
    { kod: "E.4", ad: "SOL YAN PANEL" },
    { kod: "E.5", ad: "ARKA SOL KAPAK" },
    { kod: "E.6", ad: "ARKA SAĞ KAPAK" },
    { kod: "F.1", ad: "YAKIT DEPOSU" },
    { kod: "F.2", ad: "GİDON" },
    { kod: "F.3", ad: "KAFA DEMİRİ" },
    { kod: "F.4", ad: "ŞASİ" },
];

// Araç türü ve kodu eşleşmeleri
export const ARAC_TURU_LISTESI = [
    { kod: "A", ad: "Otomobil" },
    { kod: "A", ad: "Taksi" },
    { kod: "B", ad: "Minibüs" },
    { kod: "B", ad: "Otobüs" },
    { kod: "C", ad: "Kamyonet" },
    { kod: "C", ad: "Kamyon" },
    { kod: "C", ad: "Çekici" },
    { kod: "D", ad: "İş makinesi" },
    { kod: "D", ad: "Traktör" },
    { kod: "D", ad: "Tarım makinesi" },
    { kod: "Ç", ad: "Özel amaçlı araç" },
    { kod: "E", ad: "Römork" },
    { kod: "F", ad: "Motosiklet" },
];

export const ISLEM_TURU_DEGISEN = [
    { value: "degisim_tam_boya", label: "DEĞİŞİMTAM BOYA" },
    { value: "hafif_lokal_boya", label: "LOKAL BOYA, HAFİF HASAR" },
    { value: "hafif_tam_boya", label: "TAM BOYA, HAFİF HASAR" },
    { value: "orta_lokal_boya", label: "LOKAL BOYA, ORTA HASAR" },
    { value: "orta_tam_boya", label: "TAM BOYA, ORTA HASAR" },
    { value: "yuksek_lokal_boya", label: "LOKAL BOYA, YÜKSEK HASAR" },
    { value: "yuksek_tam_boya", label: "TAM BOYA, YÜKSEK HASAR" },
];

export const ISLEM_TURU_ONARIM = [
    { value: "onarim", label: "Onarım" },
    { value: "boya", label: "Boya" }
];

export const ONARIM_SEVIYELERI = [
    { value: "hafif", label: "Hafif" },
    { value: "orta", label: "Orta" },
    { value: "yuksek", label: "Yüksek" }
];

export const BOYA_SEVIYELERI = [
    { value: "tam", label: "Tam" },
    { value: "lokal", label: "Lokal" }
];
