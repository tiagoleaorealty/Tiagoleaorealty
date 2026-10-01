#!/usr/bin/env python3
"""Generates the Finca Herradura buyer presentation in English and Spanish.

    python3 scripts/build-herradura.py

Writes /herradura/index.html (English) and /herradura/es/index.html (Spanish)
from the one template below. Edit copy in the T dictionary: every entry is
(English, Spanish). The generated pages are committed; Vercel does not run this.
"""
import os, re, json, html
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://soldbytiago.com/herradura/"
PRICE = "$16,500,000"
PHONE = "50683028660"
PHONE_PRETTY = "+506 8302 8660"
EMAIL = "tiago@soldbytiago.com"
MAPS = "https://maps.app.goo.gl/zqxicqRuNh4RcKf18"
MAPBOX_TOKEN = "pk.eyJ1IjoidGlhZ29sZWFvcmVhbHR5IiwiYSI6ImNtcThwNHVqcDBjNm0yc3BxZ3Njc25tcXkifQ.BBoP6va0fmx0mRdLZ2_tzw"

# key: (English, Spanish)
T = {
 "lang": ("en", "es"),
 "og_locale": ("en_US", "es_CR"),
 "url": (BASE, BASE + "es/"),
 "og_image": (BASE + "img/og-en.jpg", BASE + "img/og-es.jpg"),
 "title": ("204-Acre Ocean-View Development Land in Herradura, Costa Rica | $16,500,000",
           "Finca de 82.5 hectáreas con vista al mar en Herradura, Costa Rica | $16,500,000"),
 "desc": ("82.5 hectares (204 acres) of ocean-view development land in Herradura, on Costa Rica's Central Pacific. 2 km from Los Sueños Resort and Marina, 8 minutes from Jacó. Residential and commercial land use, water availability for up to 500 homes. USD $16,500,000.",
          "82.5 hectáreas de tierra para desarrollo con vista al mar en Herradura, Pacífico Central de Costa Rica. A 2 km de Los Sueños Resort y Marina y a 8 minutos de Jacó. Uso de suelo residencial y comercial, disponibilidad de agua para hasta 500 viviendas. USD $16,500,000."),
 "og_title": ("Finca Herradura: 204 acres above the Pacific, 2 km from Los Sueños",
              "Finca Herradura: 82.5 hectáreas sobre el Pacífico, a 2 km de Los Sueños"),
 "og_desc": ("Ocean-view development land in Herradura, Costa Rica. Residential and commercial land use, water for up to 500 homes. USD $16,500,000.",
             "Tierra para desarrollo con vista al mar en Herradura, Costa Rica. Uso de suelo residencial y comercial, agua para hasta 500 viviendas. USD $16,500,000."),
 "ld_name": ("Finca Herradura: 204-acre ocean-view development land", "Finca Herradura: 82.5 hectáreas para desarrollo con vista al mar"),

 # header
 "nav_overview": ("Overview", "Resumen"),
 "nav_potential": ("Potential", "Potencial"),
 "nav_location": ("Location", "Ubicación"),
 "nav_land": ("The Land", "La Finca"),
 "nav_details": ("Details", "Detalles"),
 "nav_cta": ("Inquire", "Consultar"),
 "lang_label": ("Language", "Idioma"),
 "home_label": ("soldbytiago Real Estate Group, home", "soldbytiago Real Estate Group, inicio"),

 # hero
 "hero_kicker": ("Herradura · Central Pacific · Costa Rica", "Herradura · Pacífico Central · Costa Rica"),
 "hero_h1": ("204 acres above the Pacific, minutes from Los Sueños", "82.5 hectáreas sobre el Pacífico, a minutos de Los Sueños"),
 "hero_sub": ("An ocean-view development estate with residential and commercial land use, water availability for up to 500 homes, and the Central Pacific's premier marina resort two kilometers away.",
              "Una finca para desarrollo con vista al mar, uso de suelo residencial y comercial, disponibilidad de agua para hasta 500 viviendas, y el principal resort con marina del Pacífico Central a dos kilómetros."),
 "hero_alt": ("Sunset over the Pacific seen from the upper land of Finca Herradura", "Atardecer sobre el Pacífico visto desde la parte alta de Finca Herradura"),
 "offered": ("Offered at", "Precio"),
 "btn_package": ('Schedule a site visit',
   'Agendar una visita'),
 "btn_explore": ("Explore the land", "Conocer la finca"),
 "f1_n": ("204 acres", "82.5 ha"),
 "f1_l": ("82.5 hectares in one property", "204 acres en una sola propiedad"),
 "f2_n": ("500 homes", "500 viviendas"),
 "f2_l": ("Water availability for the project", "Disponibilidad de agua para el proyecto"),
 "f3_n": ("2 km", "2 km"),
 "f3_l": ("To Los Sueños Resort and Marina", "De Los Sueños Resort y Marina"),
 "f4_n": ("8 min", "8 min"),
 "f4_l": ("To Jacó Beach", "De Playa Jacó"),

 # overview
 "ov_kicker": ("The Opportunity", "La Oportunidad"),
 "ov_h2": ("Scale like this, this close to everything, is rare on the Central Pacific.",
           "Una escala así, tan cerca de todo, es difícil de encontrar en el Pacífico Central."),
 "ov_p1": ("Finca Herradura is 82.5 hectares of rolling pasture and forested ridgeline with ocean views, public road frontage and internal roads already in place. Los Sueños Resort and Marina is two kilometers away, Jacó is eight minutes down the road, and the supermarket is one minute from the gate.",
           "Finca Herradura son 82.5 hectáreas de potrero ondulado y filas boscosas con vista al mar, frente a calle pública y caminos internos ya abiertos. Los Sueños Resort y Marina está a dos kilómetros, Jacó a ocho minutos y el supermercado a un minuto de la entrada."),
 "ov_p2": ("The land has residential and commercial land use, water availability for a project of up to 500 homes, and electrical service available. It is the scale a master-planned community, a resort or a phased mixed-use project needs, in a corridor where the buyers, the marina and the highway to San José already exist.",
           "La finca cuenta con uso de suelo residencial y comercial, disponibilidad de agua para un proyecto de hasta 500 viviendas y disponibilidad eléctrica. Es la escala que necesita una comunidad planificada, un resort o un proyecto mixto por etapas, en un corredor donde los compradores, la marina y la autopista a San José ya existen."),
 "view_alt": ("View toward Jacó Beach and the Pacific from the ridge of the property", "Vista hacia Playa Jacó y el Pacífico desde la fila de la finca"),
 "view_cap": ("From the ridge: Jacó Beach and the open Pacific.", "Desde la fila: Playa Jacó y el Pacífico abierto."),

 # potential
 "po_kicker": ("Development Potential", "Potencial de Desarrollo"),
 "po_h2": ("Land use that welcomes what this corridor is asking for.", "Un uso de suelo que permite lo que este corredor está pidiendo."),
 "po_sub": ("Residential and commercial land use opens the door to condominium communities, towers, hotels and everything tied to tourism.",
            "El uso de suelo residencial y comercial permite desarrollar condominios, torres, hoteles y todo lo asociado al turismo."),
 "po1_t": ("Residential community", "Comunidad residencial"),
 "po1_p": ("Open, rolling ground for a gated master-planned community of homes, villas and condominiums, built in phases.",
           "Terreno abierto y ondulado para una comunidad planificada de casas, villas y condominios, desarrollada por etapas."),
 "po2_t": ("Ocean-view towers", "Torres con vista al mar"),
 "po2_p": ("Ridgelines that look over Jacó and the Pacific, a natural setting for condominium towers and branded residences.",
           "Filas con vista hacia Jacó y el Pacífico, el sitio natural para torres de condominios y residencias de marca."),
 "po3_t": ("Hotel and resort", "Hotel y resort"),
 "po3_p": ("Hospitality and tourism projects fit the land use, next door to the best-known resort and marina on the Central Pacific.",
           "Los proyectos hoteleros y turísticos caben dentro del uso de suelo, junto al resort y la marina más reconocidos del Pacífico Central."),
 "po4_t": ("Commercial frontage", "Frente comercial"),
 "po4_p": ("Public road frontage by Route 34, one minute from Plaza Herradura, for retail and services that serve the project and the town.",
           "Frente a calle pública junto a la Ruta 34, a un minuto de Plaza Herradura, para comercio y servicios que atiendan al proyecto y al pueblo."),

 # location
 "lo_kicker": ("Location", "Ubicación"),
 "lo_h2": ("At the center of Costa Rica's Central Pacific.", "En el centro del Pacífico Central de Costa Rica."),
 "lo_sub": ("Herradura is the closest beach corridor to San José. The marina, the golf course, the supermarkets and the highway to the capital are all within minutes of the property.",
            "Herradura es el corredor de playa más cercano a San José. La marina, el campo de golf, los supermercados y la autopista a la capital están a minutos de la finca."),
 "d1_n": ("1", "1"), "d1_u": ("min", "min"),
 "d1_t": ("Plaza Herradura", "Plaza Herradura"),
 "d1_p": ("Auto Mercado supermarket, banks, restaurants and services", "Supermercado Auto Mercado, bancos, restaurantes y servicios"),
 "d2_n": ("6", "6"), "d2_u": ("min", "min"),
 "d2_t": ("Los Sueños Resort and Marina", "Los Sueños Resort y Marina"),
 "d2_p": ("Marina, Marriott resort, golf course and Marina Village, 2 km away", "Marina, resort Marriott, campo de golf y Marina Village, a 2 km"),
 "d3_n": ("8", "8"), "d3_u": ("min", "min"),
 "d3_t": ("Jacó Beach", "Playa Jacó"),
 "d3_p": ("The Central Pacific's main beach town: surf, dining and nightlife", "El principal pueblo de playa del Pacífico Central: surf, gastronomía y vida nocturna"),
 "d4_n": ("1:30", "1:30"), "d4_u": ("h", "h"),
 "d4_t": ("San José International Airport (SJO)", "Aeropuerto Internacional de San José (SJO)"),
 "d4_p": ("By highway via Route 27", "Por autopista, vía Ruta 27"),
 "map_aria": ("Satellite map showing Finca Herradura, Los Sueños, Plaza Herradura and Jacó", "Mapa satelital con Finca Herradura, Los Sueños, Plaza Herradura y Jacó"),
 "map_link": ("Open in Google Maps", "Abrir en Google Maps"),
 "map_note": ("Marker shows the approximate location of the property.", "El marcador indica la ubicación aproximada de la finca."),
 "mk_prop": ("Finca Herradura", "Finca Herradura"),
 "mk_ls": ("Los Sueños Marina", "Marina Los Sueños"),
 "mk_plaza": ("Plaza Herradura", "Plaza Herradura"),
 "mk_jaco": ("Jacó Beach", "Playa Jacó"),
 "ls_kicker": ("The Neighbor", "El Vecino"),
 "ls_h3": ("Los Sueños Resort and Marina, two kilometers away.", "Los Sueños Resort y Marina, a dos kilómetros."),
 "ls_p": ("An international marina, a Marriott resort, an 18-hole golf course and the restaurants and shops of Marina Village. It is the anchor every developer and every buyer in this corridor already knows.",
          "Una marina internacional, un resort Marriott, un campo de golf de 18 hoyos y los restaurantes y tiendas de Marina Village. Es el ancla que todo desarrollador y todo comprador de este corredor ya conoce."),
 "ls1_alt": ("Entrance to Los Sueños Resort", "Entrada de Los Sueños Resort"),
 "ls2_alt": ("Sport-fishing boats at the Los Sueños marina at sunset", "Lanchas de pesca deportiva en la marina de Los Sueños al atardecer"),
 "ls3_alt": ("Restaurants at Los Sueños Marina Village", "Restaurantes en Marina Village de Los Sueños"),

 # land
 "la_kicker": ("The Land", "La Finca"),
 "la_h2": ("825,380 m² on a single survey plan.", "825,380 m² en un solo plano."),
 "la_sub": ("Open pasture for building, forested ridges for the views, and a creek running through the middle. Internal roads already connect the lower land to the high ground.",
            "Potrero abierto para construir, filas boscosas para las vistas y una quebrada que cruza por el centro. Los caminos internos ya conectan la parte baja con la parte alta."),
 "plan_alt": ("Survey plan of Finca Herradura showing 825,380.70 square meters, with pasture, forest, internal roads and public road frontage",
              "Plano de Finca Herradura con 825,380.70 metros cuadrados, con potrero, montaña, caminos internos y frente a calle pública"),
 "plan_cap": ("Survey plan, 825,380.70 m². Labels appear as drawn by the surveyor.", "Plano de agrimensura, 825,380.70 m². Las etiquetas aparecen tal como las dibujó el topógrafo."),
 "lg1_t": ("Potrero", "Potrero"), "lg1_p": ("Open, rolling pasture. The easiest ground to build on and the largest share of the property.", "Pasto abierto y ondulado. El terreno más fácil de construir y la mayor parte de la finca."),
 "lg2_t": ("Montaña", "Montaña"), "lg2_p": ("Forested hillside and ridgeline along the east side. Elevation, privacy and the ocean views.", "Ladera y fila boscosa en el costado este. Altura, privacidad y las vistas al mar."),
 "lg3_t": ("Tacotal", "Tacotal"), "lg3_p": ("Young regrowth along the southern boundary.", "Vegetación joven en el lindero sur."),
 "lg4_t": ("Calle pública", "Calle pública"), "lg4_p": ("Frontage on the paved public road on the west side, by Route 34.", "Frente a la calle pública asfaltada en el costado oeste, junto a la Ruta 34."),
 "lg5_t": ("Camino interno", "Camino interno"), "lg5_p": ("Internal roads already cut across the property.", "Caminos internos ya abiertos dentro de la finca."),
 "lg6_t": ("Quebrada", "Quebrada"), "lg6_p": ("A creek crosses the land, a natural green corridor for a master plan.", "Una quebrada cruza la finca, un corredor verde natural para el plan maestro."),
 "ga_h3": ("On the ground", "En el terreno"),
 "ga_open": ("Open photo", "Abrir foto"),
 "g_sunset": ("Sunset over the Pacific from the upper land", "Atardecer sobre el Pacífico desde la parte alta"),
 "g_jaco": ("View toward Jacó Beach", "Vista hacia Playa Jacó"),
 "g_valley": ("Looking down over Herradura", "Vista hacia Herradura"),
 "g_ridge": ("Internal road along the ridge", "Camino interno sobre la fila"),
 "g_hillside": ("Open hillside", "Ladera abierta"),
 "g_dusk": ("The Pacific at dusk", "El Pacífico al anochecer"),
 "g_pad": ("Cleared, level ground", "Terreno limpio y plano"),
 "g_forest": ("Shaded internal road", "Camino interno bajo los árboles"),
 "g_road": ("Paved public road at the frontage", "Calle pública asfaltada en el frente"),
 "g_hills": ("Rolling hills at the edge of town", "Colinas al borde del pueblo"),
 "lb_close": ("Close", "Cerrar"), "lb_prev": ("Previous photo", "Foto anterior"), "lb_next": ("Next photo", "Foto siguiente"),
 "lb_label": ("Photo viewer", "Visor de fotos"),

 # details
 "de_kicker": ("Property Details", "Detalles de la Propiedad"),
 "de_h2": ("The facts a developer asks for first.", "Los datos que un desarrollador pide primero."),
 "r1_l": ("Land area", "Área"), "r1_v": ("825,380.70 m² · 82.5 hectares · 204 acres", "825,380.70 m² · 82.5 hectáreas · 204 acres"),
 "r2_l": ("Location", "Ubicación"), "r2_v": ("Herradura, Garabito, Puntarenas. 2 km from Los Sueños Resort and Marina", "Herradura, Garabito, Puntarenas. A 2 km de Los Sueños Resort y Marina"),
 "r3_l": ("Land use", "Uso de suelo"), "r3_v": ("Residential and commercial: condominiums, towers, hotels and tourism-related development", "Residencial y comercial: condominios, torres, hoteles y desarrollo asociado al turismo"),
 "r4_l": ("Water", "Agua"), "r4_v": ("Availability for a project of up to 500 homes", "Disponibilidad para un proyecto de hasta 500 viviendas"),
 "r5_l": ("Electricity", "Electricidad"), "r5_v": ("Electrical service available", "Disponibilidad eléctrica"),
 "r6_l": ("Access", "Acceso"), "r6_v": ("Paved public road frontage, internal roads in place", "Frente a calle pública asfaltada, caminos internos abiertos"),
 "r7_l": ("Ownership", "Propiedad"), "r7_v": ("Held in one Costa Rican corporation with a single shareholder", "A nombre de una sociedad anónima costarricense con un único accionista"),
 "r8_l": ("Survey", "Plano"), "r8_v": ("Three properties being joined into one plan and one title. The new survey is complete", "Tres fincas en proceso de reunirse en un solo plano y una sola finca. El plano nuevo ya está levantado"),
 "r9_l": ("Property taxes", "Impuestos"), "r9_v": ("Paid through 2026", "Pagados todo el 2026"),
 "de_note": ('Ask us for the survey plan and any further detail on the property.',
   'Consúltenos por el plano y cualquier otro detalle de la propiedad.'),

 # price
 "pr_kicker": ("Offered At", "Precio de Venta"),
 "pr_per": ("About $20 per square meter", "Aproximadamente $20 por metro cuadrado"),
 "pr_m1": ("≈ $200,000 per hectare", "≈ $200,000 por hectárea"),
 "pr_m2": ("≈ $81,000 per acre", "≈ $81,000 por acre"),
 "pr_m3": ("82.5 hectares · 204 acres", "82.5 hectáreas · 204 acres"),

 # agents
 "ag_kicker": ("Presented By", "Presentado Por"),
 "ag_h2": ("Two agents, two countries, one conversation.", "Dos agentes, dos países, una sola conversación."),
 "ag_sub": ("A team on the ground in Costa Rica and in the United States, so you can evaluate the property in your language and your time zone.",
            "Un equipo en Costa Rica y en Estados Unidos, para que evalúe la propiedad en su idioma y en su zona horaria."),
 "a1_firm": ("soldbytiago Real Estate Group · Costa Rica", "soldbytiago Real Estate Group · Costa Rica"),
 "a1_role": ("Your contact on the ground", "Su contacto en el terreno"),
 "a1_p": ("Five years in the Costa Rican market, working in English, Spanish and Portuguese. Tiago leads site visits, documents and direct communication with the owner.",
          "Cinco años en el mercado costarricense, trabajando en español, inglés y portugués. Tiago coordina las visitas a la finca, la documentación y la comunicación directa con el propietario."),
 "a2_firm": ("LoKation Real Estate · Florida, USA", "LoKation Real Estate · Florida, EE. UU."),
 "a2_role": ("U.S. investors and developers", "Inversionistas y desarrolladores en EE. UU."),
 "a2_p": ("A Florida-licensed agent based in the United States. Gabriel is the point of contact for North American investors and developers, presenting the property in your market.",
          "Agente licenciado en Florida y radicado en Estados Unidos. Gabriel es el punto de contacto para inversionistas y desarrolladores norteamericanos, presentando la propiedad en su mercado."),
 "call": ("Call", "Llamar"),
 "wa": ("WhatsApp", "WhatsApp"), "email": ("Email", "Correo"),

 # cta
 "ct_kicker": ("Next Step", "Siguiente Paso"),
 "ct_h2": ("Come walk the land", "Venga a recorrer la finca"),
 "ct_p": ('Schedule a private site visit or ask us anything about the property. We answer in English, Spanish and Portuguese.',
   'Agende una visita privada a la finca o consúltenos lo que necesite sobre la propiedad. Atendemos en español, inglés y portugués.'),
 "ct_b1": ("Message us on WhatsApp", "Escríbanos por WhatsApp"),
 "ct_b2": ("Request by email", "Solicitar por correo"),
 "wa_msg": ("Hi Tiago, I'd like more information about Finca Herradura (82.5 ha, Herradura, Costa Rica).",
   'Hola Tiago, me gustaría recibir más información sobre Finca Herradura (82.5 ha, Herradura, Costa Rica).'),
 "wa_visit": ("Hi Tiago, I'd like to schedule a site visit to Finca Herradura.", "Hola Tiago, me gustaría agendar una visita a Finca Herradura."),
 "mail_subj": ('Finca Herradura: site visit request',
   'Finca Herradura: solicitud de visita'),
 "wa_float": ("Chat on WhatsApp", "Escribir por WhatsApp"),

 # footer
 "ft_addr": ("Finca Herradura · Herradura, Garabito, Puntarenas, Costa Rica", "Finca Herradura · Herradura, Garabito, Puntarenas, Costa Rica"),
 "ft_fine": ("Offered at USD $16,500,000. Information provided by the owner and deemed reliable but not guaranteed. Areas, distances and drive times are approximate. © 2026 soldbytiago Real Estate Group.",
             "Precio de venta: USD $16,500,000. Información suministrada por el propietario, considerada confiable pero no garantizada. Las áreas, distancias y tiempos de traslado son aproximados. © 2026 soldbytiago Real Estate Group."),
}

GALLERY = [  # (file, caption key, big?)
 ("sunset-bay", "g_sunset", True), ("jaco-view", "g_jaco", False), ("valley-view", "g_valley", False),
 ("ridge-road", "g_ridge", False), ("hillside", "g_hillside", False), ("ocean-dusk", "g_dusk", True),
 ("building-pad", "g_pad", False), ("forest-road", "g_forest", False), ("public-road", "g_road", False),
 ("hills", "g_hills", False),
]

TEMPLATE = r"""<!DOCTYPE html>
<html lang="[[lang]]">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[[title]]</title>
<meta name="description" content="[[desc]]">
<link rel="canonical" href="[[url]]">
<link rel="alternate" hreflang="en" href="{{BASE}}">
<link rel="alternate" hreflang="es" href="{{BASE}}es/">
<link rel="alternate" hreflang="x-default" href="{{BASE}}">
<meta name="theme-color" content="#2d422d">
<meta property="og:type" content="website">
<meta property="og:site_name" content="soldbytiago Real Estate Group">
<meta property="og:locale" content="[[og_locale]]">
<meta property="og:title" content="[[og_title]]">
<meta property="og:description" content="[[og_desc]]">
<meta property="og:url" content="[[url]]">
<meta property="og:image" content="[[og_image]]">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="[[og_image]]">
<link rel="icon" type="image/png" href="/favicon-48.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/herradura/img/hero.jpg" as="image" media="(min-width: 701px)">
<link rel="preload" href="/herradura/img/hero-m.jpg" as="image" media="(max-width: 700px)">
<link rel="preload" href="/neue-haas-grotesk-display-pro-cufonfonts/NeueHaasDisplayBold.ttf" as="font" type="font/ttf" crossorigin>
<link rel="preload" href="/neue-haas-grotesk-display-pro-cufonfonts/NeueHaasDisplayRoman.ttf" as="font" type="font/ttf" crossorigin>
<script type="application/ld+json">
{{JSONLD}}
</script>
<style>
/* Brand palette (2026-09): green #2d422d, charcoal #30312f, terracotta #d37234 (accents only), cream #efeae3 (cards on green) */
:root{
  --green:#2d422d; --green-mid:#233423; --green-deep:#1c291c;
  --ink:#30312f; --body:#454842; --muted:#5c6058;
  --terra:#d37234; --terra-ink:#984916; --terra-soft:#e5945c;
  --cream:#efeae3; --sage:#b1b7a9; --line:rgba(48,49,47,.13);
  --wa:#25d366;
  --pad:clamp(1.25rem,4.5vw,3.5rem);
  --sec:clamp(76px,10vw,140px);
}
@font-face{font-family:"Neue Haas";src:url("/neue-haas-grotesk-display-pro-cufonfonts/NeueHaasDisplayLight.ttf") format("truetype");font-weight:300;font-display:swap}
@font-face{font-family:"Neue Haas";src:url("/neue-haas-grotesk-display-pro-cufonfonts/NeueHaasDisplayRoman.ttf") format("truetype");font-weight:400;font-display:swap}
@font-face{font-family:"Neue Haas";src:url("/neue-haas-grotesk-display-pro-cufonfonts/NeueHaasDisplayMediu.ttf") format("truetype");font-weight:500;font-display:swap}
@font-face{font-family:"Neue Haas";src:url("/neue-haas-grotesk-display-pro-cufonfonts/NeueHaasDisplayBold.ttf") format("truetype");font-weight:700;font-display:swap}

*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{
  font-family:"Neue Haas","Neue Haas Grotesk Display Pro","Helvetica Neue",Helvetica,Arial,sans-serif;
  background:#fff;color:var(--body);font-size:17px;line-height:1.65;font-weight:400;
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;overflow-x:hidden;
}
img{display:block;max-width:100%}
a{color:inherit}
a,button{-webkit-tap-highlight-color:transparent;touch-action:manipulation}
::selection{background:var(--green);color:#fff}
.wrap{max-width:1280px;margin-inline:auto;padding-inline:var(--pad)}
section{scroll-margin-top:70px}
h1,h2,h3{color:var(--ink);text-wrap:balance}
p{text-wrap:pretty}
.sq{display:inline-block;width:.2em;height:.2em;background:var(--terra);margin-left:.07em}

.kicker{
  display:flex;align-items:center;gap:14px;
  font-size:12px;font-weight:500;letter-spacing:.2em;text-transform:uppercase;color:var(--terra-ink);
}
.kicker::before{content:"";width:10px;height:10px;background:var(--terra);flex:none}
.h2{font-weight:700;letter-spacing:-.032em;line-height:1.04;font-size:clamp(2.1rem,4.6vw,3.75rem)}
.sub{font-size:clamp(17px,1.5vw,19.5px);color:var(--muted);max-width:60ch;margin-top:22px}
.dark{background:var(--green);color:rgba(239,234,227,.82)}
.dark h2,.dark h3{color:#fff}
.dark .kicker{color:var(--terra-soft)}
.dark .sub{color:rgba(239,234,227,.78)}
.head{display:grid;gap:18px;max-width:900px}

.btn{
  display:inline-flex;align-items:center;justify-content:center;gap:10px;
  padding:16px 28px;border-radius:999px;border:1px solid transparent;
  font-family:inherit;font-size:12.5px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;
  text-decoration:none;cursor:pointer;text-align:center;
  transition:background .25s,color .25s,border-color .25s,transform .25s;
}
.btn svg{width:16px;height:16px;flex:none}
.btn-white{background:#fff;color:var(--ink)}
.btn-white:hover{background:var(--cream)}
.btn-line{border-color:rgba(255,255,255,.5);color:#fff}
.btn-line:hover{border-color:#fff;background:rgba(255,255,255,.08)}
.btn-green{background:var(--green);color:#fff}
.btn-green:hover{background:var(--green-deep)}
.btn-ghost{border-color:rgba(48,49,47,.3);color:var(--ink)}
.btn-ghost:hover{border-color:var(--ink)}
.btn:active{transform:scale(.98)}
a:focus-visible,button:focus-visible{outline:2px solid var(--terra);outline-offset:3px}

/* reveal (only when JS is running) */
.js .rv{opacity:0;transform:translateY(22px);transition:opacity .8s cubic-bezier(.2,.7,.2,1),transform .8s cubic-bezier(.2,.7,.2,1)}
.js .rv.on{opacity:1;transform:none}
.js .rv.d1{transition-delay:.08s}.js .rv.d2{transition-delay:.16s}.js .rv.d3{transition-delay:.24s}

/* ── header ── */
header{position:fixed;inset:0 0 auto 0;z-index:60;transition:background .35s,box-shadow .35s}
.hd{max-width:1440px;margin-inline:auto;padding:16px var(--pad);display:flex;align-items:center;gap:24px}
.brands{display:flex;align-items:center;gap:clamp(12px,1.6vw,20px);text-decoration:none;flex:none}
.brands img{height:30px;width:auto}
.brands .lok{height:21px}
.brands i{width:1px;height:26px;background:rgba(255,255,255,.4);transition:background .35s}
.brands .on-light{display:none}
.hnav{display:flex;gap:26px;margin-left:auto;font-size:13px;letter-spacing:.04em}
.hnav a{text-decoration:none;color:rgba(255,255,255,.88);transition:color .25s}
.hnav a:hover{color:#fff}
.hright{display:flex;align-items:center;gap:12px;flex:none}
.lang{display:flex;padding:3px;border-radius:999px;border:1px solid rgba(255,255,255,.45);transition:border-color .35s}
.lang a{
  min-width:40px;padding:6px 11px;border-radius:999px;text-align:center;text-decoration:none;
  font-size:12px;font-weight:500;letter-spacing:.1em;color:rgba(255,255,255,.9);transition:background .25s,color .25s;
}
.lang a[aria-current="true"]{background:#fff;color:var(--ink)}
.hd .btn{padding:11px 20px;font-size:11.5px}
header.scrolled{background:rgba(255,255,255,.94);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);box-shadow:0 1px 0 var(--line)}
header.scrolled .brands .on-dark{display:none}
header.scrolled .brands .on-light{display:block}
header.scrolled .brands i{background:var(--line)}
header.scrolled .hnav a{color:var(--muted)}
header.scrolled .hnav a:hover{color:var(--ink)}
header.scrolled .lang{border-color:rgba(48,49,47,.25)}
header.scrolled .lang a{color:var(--muted)}
header.scrolled .lang a[aria-current="true"]{background:var(--green);color:#fff}
header.scrolled .btn-white{background:var(--green);color:#fff}
@media(max-width:1080px){.hnav{display:none}.hright{margin-left:auto}}
@media(max-width:640px){
  .hd{padding-block:13px;gap:10px}
  .hd .btn{display:none}
  .brands img{height:23px}.brands .lok{height:15px}.brands i{height:20px}
  .lang a{min-width:34px;padding:5px 8px;font-size:11px}
}
@media(max-width:370px){.brands img{height:20px}.brands .lok{height:13px}.brands{gap:9px}}

/* ── hero ── */
.hero{position:relative;min-height:100svh;display:flex;flex-direction:column;justify-content:flex-end;color:#fff;overflow:hidden;background:var(--green-deep)}
.hero picture{position:absolute;inset:0}
.hero .bg{width:100%;height:100%;object-fit:cover;object-position:center 42%;animation:settle 2.6s cubic-bezier(.2,.7,.2,1) both}
@keyframes settle{from{transform:scale(1.07)}to{transform:scale(1)}}
.hero::after{
  content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(to top,rgba(20,30,20,.94) 0%,rgba(20,30,20,.6) 30%,rgba(20,30,20,.1) 60%,rgba(20,30,20,.38) 100%);
}
.hero-in{position:relative;z-index:2;width:100%;max-width:1280px;margin-inline:auto;padding:130px var(--pad) 0}
.hero .kicker{color:#fff}
.hero h1{
  color:#fff;font-weight:700;letter-spacing:-.04em;line-height:.98;
  font-size:clamp(2.7rem,7.3vw,6.4rem);margin:22px 0 22px;max-width:15ch;
}
.hero .lede{font-size:clamp(16.5px,1.6vw,20px);line-height:1.55;color:rgba(255,255,255,.88);max-width:56ch}
.hero-row{display:flex;flex-wrap:wrap;align-items:center;gap:22px 38px;margin-top:34px}
.price-tag small{display:block;font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;color:rgba(255,255,255,.72);font-weight:500}
.price-tag b{display:block;font-size:clamp(28px,3.4vw,42px);font-weight:700;letter-spacing:-.03em;line-height:1.1;font-variant-numeric:tabular-nums}
.hero-ctas{display:flex;flex-wrap:wrap;gap:12px}
.facts{
  position:relative;z-index:2;width:100%;max-width:1280px;margin:clamp(40px,6vh,70px) auto 0;padding:0 var(--pad);
}
.facts ul{list-style:none;display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid rgba(255,255,255,.28)}
.facts li{padding:22px 22px 30px 0}
.facts li+li{padding-left:22px;border-left:1px solid rgba(255,255,255,.18)}
.facts b{display:block;color:#fff;font-size:clamp(22px,2.6vw,34px);font-weight:700;letter-spacing:-.03em;line-height:1.1}
.facts span{display:block;margin-top:7px;font-size:13px;line-height:1.4;color:rgba(255,255,255,.74)}
@media(max-width:820px){
  .facts ul{grid-template-columns:1fr 1fr}
  .facts li{padding:16px 14px 18px 0}
  .facts li+li{padding-left:0;border-left:none}
  .facts li:nth-child(even){padding-left:16px;border-left:1px solid rgba(255,255,255,.18)}
  .facts li:nth-child(n+3){border-top:1px solid rgba(255,255,255,.18)}
  .facts li:nth-child(n+3){padding-bottom:26px}
}
@media(max-width:700px){
  .hero .bg{object-position:center center}
  .hero-in{padding-top:110px}
  .hero-ctas{width:100%}
  .hero-ctas .btn{flex:1 1 100%}
}

/* ── overview ── */
.overview{padding:var(--sec) 0 0}
.ov-grid{display:grid;grid-template-columns:1.05fr 1fr;gap:clamp(32px,6vw,96px);align-items:start}
.ov-grid .kicker{margin-bottom:22px}
.ov-text p{font-size:clamp(17.5px,1.55vw,20px);line-height:1.62}
.ov-text p+p{margin-top:1.2em}
.ov-text p:first-child{color:var(--ink)}
@media(max-width:900px){.ov-grid{grid-template-columns:1fr}}
.viewband{margin-top:var(--sec);position:relative;height:clamp(340px,62vw,720px);overflow:hidden;background:var(--green-deep)}
.viewband img{width:100%;height:100%;object-fit:cover;object-position:center 30%}
.viewband figcaption{
  position:absolute;inset:auto 0 0 0;padding:90px var(--pad) 26px;color:#fff;font-size:14px;letter-spacing:.02em;
  background:linear-gradient(to top,rgba(20,30,20,.7),transparent);
}
.viewband figcaption span{display:block;max-width:1280px;margin-inline:auto}

/* ── potential ── */
.potential{padding:var(--sec) 0}
.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:clamp(40px,5vw,64px)}
.card{background:var(--cream);color:var(--body);border-radius:4px;padding:30px 26px 34px;display:flex;flex-direction:column;min-height:270px}
.card .no{font-size:12px;font-weight:500;letter-spacing:.18em;color:var(--terra-ink)}
.card h3{color:var(--ink);font-size:23px;font-weight:700;letter-spacing:-.025em;line-height:1.12;margin:auto 0 12px;padding-top:56px}
.card p{font-size:15.5px;line-height:1.55;color:var(--body)}
@media(max-width:1080px){.cards{grid-template-columns:1fr 1fr}.card{min-height:0}.card h3{padding-top:40px}}
@media(max-width:600px){.cards{grid-template-columns:1fr}.card h3{padding-top:26px}}

/* ── location ── */
.location{padding:var(--sec) 0}
.loc-grid{display:grid;grid-template-columns:1fr 1.35fr;gap:clamp(28px,4vw,64px);margin-top:clamp(40px,5vw,64px);align-items:stretch}
.drive{list-style:none;border-top:1px solid var(--line)}
.drive li{display:grid;grid-template-columns:118px 1fr;gap:18px;align-items:baseline;padding:24px 0;border-bottom:1px solid var(--line)}
.drive .t{color:var(--green);font-weight:700;letter-spacing:-.04em;line-height:1;font-size:clamp(40px,4.2vw,56px);font-variant-numeric:tabular-nums;white-space:nowrap}
.drive .t small{font-size:.34em;font-weight:500;letter-spacing:.04em;margin-left:5px;color:var(--terra-ink);text-transform:uppercase}
.drive b{display:block;color:var(--ink);font-size:18.5px;font-weight:700;letter-spacing:-.015em;line-height:1.25}
.drive span{display:block;font-size:15px;color:var(--muted);margin-top:4px;line-height:1.45}
.mapbox{position:relative;min-height:520px;border-radius:4px;overflow:hidden;background:#233423 url("/herradura/img/g/valley-view-t.jpg") center/cover}
#map{position:absolute;inset:0}
.map-foot{display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px 24px;margin-top:14px;font-size:13.5px;color:var(--muted)}
.map-foot a{color:var(--green);font-weight:500;text-decoration:none;border-bottom:1px solid currentColor;padding-bottom:1px;display:inline-flex;gap:7px;align-items:center}
.mk{display:flex;align-items:center;gap:8px;font-family:"Neue Haas",Helvetica,Arial,sans-serif;pointer-events:none}
.mk.left{flex-direction:row-reverse}
.mk i{width:12px;height:12px;border-radius:50%;background:#fff;border:3px solid var(--green);box-shadow:0 2px 8px rgba(0,0,0,.4);flex:none}
.mk span{background:#fff;color:var(--ink);font-size:12.5px;font-weight:500;padding:5px 10px;border-radius:3px;white-space:nowrap;box-shadow:0 4px 14px rgba(0,0,0,.28)}
.mk.prop i{width:20px;height:20px;background:var(--terra);border:3px solid #fff;position:relative}
.mk.prop i::after{content:"";position:absolute;inset:-12px;border-radius:50%;border:2px solid rgba(255,255,255,.75);animation:pulse 2.4s ease-out infinite}
@keyframes pulse{from{transform:scale(.5);opacity:1}to{transform:scale(1.5);opacity:0}}
.mk.prop span{background:var(--green);color:#fff;font-weight:700;font-size:13.5px;padding:7px 12px}
.mapboxgl-ctrl-attrib{font-size:10px}
@media(max-width:940px){
  .loc-grid{grid-template-columns:1fr}
  .mapbox{min-height:0;height:min(120vw,460px)}
}
@media(max-width:480px){.drive li{grid-template-columns:92px 1fr;gap:14px;padding:20px 0}}

.neighbor{margin-top:var(--sec);display:grid;grid-template-columns:1fr 1.9fr;gap:clamp(28px,4vw,64px);align-items:end}
.neighbor h3{font-size:clamp(1.6rem,2.8vw,2.3rem);font-weight:700;letter-spacing:-.03em;line-height:1.08;margin:18px 0 16px}
.neighbor p:not(.kicker){color:var(--muted);font-size:16.5px}
.trio{display:grid;grid-template-columns:1.25fr 1fr 1fr;gap:12px}
.trio a{display:block;overflow:hidden;border-radius:4px;aspect-ratio:4/5;background:var(--sage)}
.trio a:first-child{aspect-ratio:auto}
.trio img{width:100%;height:100%;object-fit:cover;transition:transform .9s cubic-bezier(.2,.7,.2,1)}
.trio a:hover img{transform:scale(1.05)}
@media(max-width:940px){.neighbor{grid-template-columns:1fr}}
@media(max-width:560px){.trio{grid-template-columns:1fr 1fr}.trio a:first-child{grid-column:1/-1;aspect-ratio:16/10}}

/* ── land ── */
.land{padding:var(--sec) 0;border-top:1px solid var(--line)}
.plan{margin-top:clamp(40px,5vw,64px);display:grid;grid-template-columns:1.7fr 1fr;gap:clamp(28px,4vw,60px);align-items:start}
.plan figure{border-radius:4px;padding:clamp(14px,2.4vw,34px);background:var(--green-mid);position:relative}
.plan figure a{display:block;cursor:zoom-in}
.plan figure img{width:100%;height:auto}
.plan figcaption{margin-top:16px;padding-top:14px;border-top:1px solid rgba(239,234,227,.2);font-size:13px;color:rgba(239,234,227,.72)}
.plan .area{position:absolute;top:clamp(14px,2.4vw,30px);left:clamp(14px,2.4vw,34px);line-height:1.1}
.plan .area{pointer-events:none}
.plan .area b{display:block;color:#fff;font-size:clamp(20px,2.6vw,34px);font-weight:700;letter-spacing:-.03em}
.plan .area span{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--terra-soft);font-weight:500}
.legend{list-style:none;border-top:1px solid var(--line)}
.legend li{padding:17px 0;border-bottom:1px solid var(--line)}
.legend b{display:block;color:var(--ink);font-size:12.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
.legend span{display:block;font-size:15.5px;line-height:1.5;color:var(--muted);margin-top:5px}
@media(max-width:940px){.plan{grid-template-columns:1fr}.plan .area{position:static;margin-bottom:10px}}
.gal-h{margin:var(--sec) 0 26px;display:flex;align-items:baseline;justify-content:space-between;gap:20px}
.gal-h h3{font-size:clamp(1.6rem,2.8vw,2.3rem);font-weight:700;letter-spacing:-.03em}
.gal-h span{font-size:13px;color:var(--muted);letter-spacing:.04em}
.gal{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:clamp(150px,19vw,250px);grid-auto-flow:dense;gap:10px}
.gal a{position:relative;display:block;overflow:hidden;border-radius:4px;background:var(--sage)}
.gal a.big{grid-column:span 2;grid-row:span 2}
.gal a.big2{grid-column:3 / span 2;grid-row:3 / span 2}
.gal img{width:100%;height:100%;object-fit:cover;transition:transform .9s cubic-bezier(.2,.7,.2,1)}
.gal a:hover img{transform:scale(1.05)}
.gal a span{
  position:absolute;inset:auto 0 0 0;padding:40px 14px 12px;color:#fff;font-size:13px;line-height:1.3;
  background:linear-gradient(to top,rgba(20,30,20,.78),transparent);opacity:0;transition:opacity .3s;
}
.gal a:hover span,.gal a:focus-visible span,.gal a.big span{opacity:1}
@media(max-width:760px){
  .gal{grid-template-columns:1fr 1fr;grid-auto-rows:42vw;gap:8px}
  .gal a.big,.gal a.big2{grid-column:1/-1;grid-row:span 1;grid-row-start:auto;height:64vw}
  .gal{grid-auto-rows:auto}
  .gal a:not(.big){aspect-ratio:1/1}
  .gal a span{opacity:1;font-size:12px;padding:30px 10px 9px}
}

/* ── details ── */
.details{padding:var(--sec) 0;background:var(--green-deep)}
.det-grid{display:grid;grid-template-columns:1fr 1.5fr;gap:clamp(32px,6vw,96px);align-items:start}
.det-grid .head{position:sticky;top:110px}
.rows{border-top:1px solid rgba(239,234,227,.2)}
.rows div{display:grid;grid-template-columns:170px 1fr;gap:20px;padding:21px 0;border-bottom:1px solid rgba(239,234,227,.2)}
.rows dt{font-size:12px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:var(--terra-soft);padding-top:4px}
.rows dd{color:#fff;font-size:clamp(17px,1.5vw,19.5px);line-height:1.45;letter-spacing:-.005em}
.det-note{margin-top:26px;font-size:14.5px;color:rgba(239,234,227,.7);max-width:56ch}
@media(max-width:940px){.det-grid{grid-template-columns:1fr}.det-grid .head{position:static}}
@media(max-width:560px){.rows div{grid-template-columns:1fr;gap:5px;padding:17px 0}}

/* ── price ── */
.price{padding:var(--sec) 0;text-align:center}
.price .kicker{justify-content:center}
.price .num{
  color:var(--green);font-weight:700;letter-spacing:-.05em;line-height:.95;
  font-size:clamp(3rem,11.5vw,9.5rem);margin:26px 0 20px;font-variant-numeric:tabular-nums;
}
.price .num sup{font-size:.26em;font-weight:500;letter-spacing:.08em;vertical-align:top;position:relative;top:.55em;margin-right:.35em;color:var(--terra-ink)}
.price .per{font-size:clamp(18px,2vw,24px);color:var(--ink);font-weight:500;letter-spacing:-.01em}
.price ul{list-style:none;display:flex;flex-wrap:wrap;justify-content:center;gap:8px 12px;margin-top:26px}
.price li{font-size:14px;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:8px 18px}

/* ── agents ── */
.agents{padding:var(--sec) 0;border-top:1px solid var(--line)}
.agent-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:clamp(40px,5vw,64px)}
.agent{border:1px solid var(--line);border-radius:4px;padding:clamp(24px,3vw,40px);display:grid;grid-template-columns:132px 1fr;gap:clamp(18px,2.4vw,32px);align-items:start}
.agent .ph{width:132px;height:132px;border-radius:50%;object-fit:cover;background:var(--sage)}
.agent .logo{height:26px;width:auto;margin-bottom:18px}
.agent .logo.lok{height:20px;margin-top:3px;margin-bottom:21px}
.agent h3{font-size:28px;font-weight:700;letter-spacing:-.03em;line-height:1.1}
.agent .role{font-size:12px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:var(--terra-ink);margin-top:8px}
.agent .firm{font-size:14px;color:var(--muted);margin-top:4px}
.agent p.bio{font-size:15.5px;line-height:1.6;margin-top:16px}
.agent .contact{display:flex;flex-wrap:wrap;gap:6px 20px;margin-top:16px;font-size:15px}
.agent .contact a{color:var(--green);font-weight:500;text-decoration:none;border-bottom:1px solid rgba(45,66,45,.35)}
.agent .actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}
.agent .actions .btn{padding:13px 22px}
@media(max-width:1000px){.agent-grid{grid-template-columns:1fr}}
@media(max-width:560px){.agent{grid-template-columns:1fr}.agent .ph{width:104px;height:104px}}

/* ── cta ── */
.cta{position:relative;padding:clamp(90px,13vw,180px) 0;text-align:center;color:#fff;overflow:hidden;background:var(--green-deep)}
.cta > img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 60%;opacity:.8}
.cta::after{content:"";position:absolute;inset:0;background:linear-gradient(rgba(28,41,28,.5),rgba(28,41,28,.82))}
.cta .wrap{position:relative;z-index:2}
.cta .kicker{justify-content:center;color:var(--terra-soft)}
.cta h2{color:#fff;font-weight:700;letter-spacing:-.04em;line-height:1;font-size:clamp(2.6rem,7vw,5.6rem);margin:22px 0}
.cta p.kicker{font-size:12px;max-width:none;color:var(--terra-soft)}
.cta p:not(.kicker){max-width:52ch;margin-inline:auto;font-size:clamp(17px,1.6vw,20px);color:rgba(255,255,255,.86)}
.cta-btns{display:flex;flex-wrap:wrap;justify-content:center;gap:12px;margin-top:36px}

footer{background:#141e14;color:rgba(239,234,227,.66);padding:60px 0 46px;font-size:13.5px;text-align:center}
footer .brands{justify-content:center;margin-bottom:26px}
footer .brands img{height:34px}footer .brands .lok{height:23px}
footer p{max-width:780px;margin:0 auto}
footer p+p{margin-top:10px}
footer .addr{color:rgba(239,234,227,.9)}
footer a{color:rgba(239,234,227,.9)}
footer .fine{font-size:12px;line-height:1.6;margin-top:18px;color:rgba(239,234,227,.5)}

.wa-float{
  position:fixed;right:20px;bottom:20px;z-index:55;width:56px;height:56px;border-radius:50%;
  background:var(--wa);display:flex;align-items:center;justify-content:center;
  box-shadow:0 8px 26px rgba(0,0,0,.28);transition:transform .25s;
}
.wa-float:hover{transform:scale(1.07)}
.wa-float svg{width:30px;height:30px;fill:#fff}

/* ── lightbox ── */
#lb{position:fixed;inset:0;z-index:100;background:#0f160f;display:none;flex-direction:column;color:#fff}
#lb.open{display:flex}
.lb-top{display:flex;justify-content:space-between;align-items:center;padding:16px 20px;font-size:13px;letter-spacing:.1em}
.lb-stage{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;position:relative;padding:0 12px}
.lb-stage img{max-width:100%;max-height:100%;object-fit:contain;border-radius:2px}
#lb button{background:rgba(255,255,255,.1);border:0;color:#fff;width:46px;height:46px;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .2s}
#lb button:hover{background:rgba(255,255,255,.22)}
.lb-nav{position:absolute;top:50%;transform:translateY(-50%)}
.lb-prev{left:16px}.lb-next{right:16px}
.lb-cap{padding:16px 20px 24px;text-align:center;font-size:15px;color:rgba(255,255,255,.85);min-height:62px}

@media (prefers-reduced-motion: reduce){
  html{scroll-behavior:auto}
  .js .rv{opacity:1;transform:none;transition:none}
  .hero .bg,.mk.prop i::after{animation:none}
  .gal img,.trio img{transition:none}
}
@media print{header,.wa-float,#lb{display:none}.js .rv{opacity:1;transform:none}}
</style>
</head>
<body>

<header id="hd">
  <div class="hd">
    <a class="brands" href="/" aria-label="[[home_label]]">
      <img class="on-dark" src="/herradura/img/logo-sbt-light.png" alt="soldbytiago Real Estate Group" width="900" height="201">
      <img class="on-light" src="/herradura/img/logo-sbt.png" alt="" width="900" height="201">
      <i aria-hidden="true"></i>
      <img class="on-dark lok" src="/herradura/img/logo-lokation-light.png" alt="LoKation Real Estate" width="812" height="149">
      <img class="on-light lok" src="/herradura/img/logo-lokation.png" alt="" width="812" height="149">
    </a>
    <nav class="hnav" aria-label="Sections">
      <a href="#overview">[[nav_overview]]</a>
      <a href="#potential">[[nav_potential]]</a>
      <a href="#location">[[nav_location]]</a>
      <a href="#land">[[nav_land]]</a>
      <a href="#details">[[nav_details]]</a>
    </nav>
    <div class="hright">
      <nav class="lang" aria-label="[[lang_label]]">
        <a href="/herradura/" lang="en" hreflang="en" title="English"{{CUR_EN}}>EN</a>
        <a href="/herradura/es/" lang="es" hreflang="es" title="Español"{{CUR_ES}}>ES</a>
      </nav>
      <a class="btn btn-white" href="#contact">[[nav_cta]]</a>
    </div>
  </div>
</header>

<main>
<section class="hero" id="top">
  <picture>
    <source media="(max-width: 700px)" srcset="/herradura/img/hero-m.jpg">
    <img class="bg" src="/herradura/img/hero.jpg" alt="[[hero_alt]]" width="1920" height="1215" fetchpriority="high">
  </picture>
  <div class="hero-in">
    <p class="kicker">[[hero_kicker]]</p>
    <h1>[[hero_h1]]<span class="sq" aria-hidden="true"></span></h1>
    <p class="lede">[[hero_sub]]</p>
    <div class="hero-row">
      <div class="price-tag"><small>[[offered]]</small><b>USD {{PRICE}}</b></div>
      <div class="hero-ctas">
        <a class="btn btn-white" href="{{WA_VISIT}}" target="_blank" rel="noopener">[[btn_package]]</a>
        <a class="btn btn-line" href="#land">[[btn_explore]]</a>
      </div>
    </div>
  </div>
  <div class="facts">
    <ul>
      <li><b>[[f1_n]]</b><span>[[f1_l]]</span></li>
      <li><b>[[f2_n]]</b><span>[[f2_l]]</span></li>
      <li><b>[[f3_n]]</b><span>[[f3_l]]</span></li>
      <li><b>[[f4_n]]</b><span>[[f4_l]]</span></li>
    </ul>
  </div>
</section>

<section class="overview" id="overview">
  <div class="wrap ov-grid">
    <div>
      <p class="kicker rv">[[ov_kicker]]</p>
      <h2 class="h2 rv d1">[[ov_h2]]</h2>
    </div>
    <div class="ov-text rv d2">
      <p>[[ov_p1]]</p>
      <p>[[ov_p2]]</p>
    </div>
  </div>
  <figure class="viewband">
    <img src="/herradura/img/g/jaco-view.jpg" alt="[[view_alt]]" width="1280" height="960" loading="lazy" decoding="async">
    <figcaption><span>[[view_cap]]</span></figcaption>
  </figure>
</section>

<section class="potential dark" id="potential">
  <div class="wrap">
    <div class="head">
      <p class="kicker rv">[[po_kicker]]</p>
      <h2 class="h2 rv d1">[[po_h2]]</h2>
      <p class="sub rv d2" style="margin-top:4px">[[po_sub]]</p>
    </div>
    <div class="cards">
      <article class="card rv"><span class="no">01</span><h3>[[po1_t]]</h3><p>[[po1_p]]</p></article>
      <article class="card rv d1"><span class="no">02</span><h3>[[po2_t]]</h3><p>[[po2_p]]</p></article>
      <article class="card rv d2"><span class="no">03</span><h3>[[po3_t]]</h3><p>[[po3_p]]</p></article>
      <article class="card rv d3"><span class="no">04</span><h3>[[po4_t]]</h3><p>[[po4_p]]</p></article>
    </div>
  </div>
</section>

<section class="location" id="location">
  <div class="wrap">
    <div class="head">
      <p class="kicker rv">[[lo_kicker]]</p>
      <h2 class="h2 rv d1">[[lo_h2]]</h2>
      <p class="sub rv d2" style="margin-top:4px">[[lo_sub]]</p>
    </div>
    <div class="loc-grid">
      <ul class="drive rv">
        <li><div class="t">[[d1_n]]<small>[[d1_u]]</small></div><div><b>[[d1_t]]</b><span>[[d1_p]]</span></div></li>
        <li><div class="t">[[d2_n]]<small>[[d2_u]]</small></div><div><b>[[d2_t]]</b><span>[[d2_p]]</span></div></li>
        <li><div class="t">[[d3_n]]<small>[[d3_u]]</small></div><div><b>[[d3_t]]</b><span>[[d3_p]]</span></div></li>
        <li><div class="t">[[d4_n]]<small>[[d4_u]]</small></div><div><b>[[d4_t]]</b><span>[[d4_p]]</span></div></li>
      </ul>
      <div class="rv d1">
        <div class="mapbox"><div id="map" role="img" aria-label="[[map_aria]]"></div></div>
        <div class="map-foot">
          <span>9.6610° N · 84.6350° W. [[map_note]]</span>
          <a href="{{MAPS}}" target="_blank" rel="noopener">[[map_link]]
            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M7 17L17 7M8 7h9v9"/></svg></a>
        </div>
      </div>
    </div>

    <div class="neighbor">
      <div class="rv">
        <p class="kicker">[[ls_kicker]]</p>
        <h3>[[ls_h3]]</h3>
        <p>[[ls_p]]</p>
      </div>
      <div class="trio rv d1">
        <a href="/herradura/img/g/los-suenos-marina.jpg" data-lb data-cap="[[ls2_alt]]"><img src="/herradura/img/g/los-suenos-marina-t.jpg" alt="[[ls2_alt]]" loading="lazy" decoding="async" width="720" height="540"></a>
        <a href="/herradura/img/g/los-suenos-gate.jpg" data-lb data-cap="[[ls1_alt]]"><img src="/herradura/img/g/los-suenos-gate-t.jpg" alt="[[ls1_alt]]" loading="lazy" decoding="async" width="720" height="540"></a>
        <a href="/herradura/img/g/marina-village.jpg" data-lb data-cap="[[ls3_alt]]"><img src="/herradura/img/g/marina-village-t.jpg" alt="[[ls3_alt]]" loading="lazy" decoding="async" width="720" height="540"></a>
      </div>
    </div>
  </div>
</section>

<section class="land" id="land">
  <div class="wrap">
    <div class="head">
      <p class="kicker rv">[[la_kicker]]</p>
      <h2 class="h2 rv d1">[[la_h2]]</h2>
      <p class="sub rv d2" style="margin-top:4px">[[la_sub]]</p>
    </div>
    <div class="plan">
      <figure class="rv">
        <div class="area"><b>825,380.70 m²</b><span>82.5 ha · 204 acres</span></div>
        <a href="/herradura/img/plan.png" data-lb data-cap="[[plan_cap]]"><img src="/herradura/img/plan.png" alt="[[plan_alt]]" width="2400" height="1662" loading="lazy" decoding="async"></a>
        <figcaption>[[plan_cap]]</figcaption>
      </figure>
      <ul class="legend rv d1">
        <li><b>[[lg1_t]]</b><span>[[lg1_p]]</span></li>
        <li><b>[[lg2_t]]</b><span>[[lg2_p]]</span></li>
        <li><b>[[lg3_t]]</b><span>[[lg3_p]]</span></li>
        <li><b>[[lg4_t]]</b><span>[[lg4_p]]</span></li>
        <li><b>[[lg5_t]]</b><span>[[lg5_p]]</span></li>
        <li><b>[[lg6_t]]</b><span>[[lg6_p]]</span></li>
      </ul>
    </div>

    <div class="gal-h rv"><h3>[[ga_h3]]</h3></div>
    <div class="gal rv">
{{GALLERY}}
    </div>
  </div>
</section>

<section class="details dark" id="details">
  <div class="wrap det-grid">
    <div class="head">
      <p class="kicker rv">[[de_kicker]]</p>
      <h2 class="h2 rv d1">[[de_h2]]</h2>
    </div>
    <div class="rv d1">
      <dl class="rows">
        <div><dt>[[r1_l]]</dt><dd>[[r1_v]]</dd></div>
        <div><dt>[[r2_l]]</dt><dd>[[r2_v]]</dd></div>
        <div><dt>[[r3_l]]</dt><dd>[[r3_v]]</dd></div>
        <div><dt>[[r4_l]]</dt><dd>[[r4_v]]</dd></div>
        <div><dt>[[r5_l]]</dt><dd>[[r5_v]]</dd></div>
        <div><dt>[[r6_l]]</dt><dd>[[r6_v]]</dd></div>
        <div><dt>[[r7_l]]</dt><dd>[[r7_v]]</dd></div>
        <div><dt>[[r8_l]]</dt><dd>[[r8_v]]</dd></div>
        <div><dt>[[r9_l]]</dt><dd>[[r9_v]]</dd></div>
      </dl>
      <p class="det-note">[[de_note]]</p>
    </div>
  </div>
</section>

<section class="price" id="price">
  <div class="wrap">
    <p class="kicker rv">[[pr_kicker]]</p>
    <p class="num rv d1"><sup>USD</sup>{{PRICE}}</p>
    <p class="per rv d2">[[pr_per]]</p>
    <ul class="rv d2">
      <li>[[pr_m3]]</li>
      <li>[[pr_m1]]</li>
      <li>[[pr_m2]]</li>
    </ul>
  </div>
</section>

<section class="agents" id="agents">
  <div class="wrap">
    <div class="head">
      <p class="kicker rv">[[ag_kicker]]</p>
      <h2 class="h2 rv d1">[[ag_h2]]</h2>
      <p class="sub rv d2" style="margin-top:4px">[[ag_sub]]</p>
    </div>
    <div class="agent-grid">
      <article class="agent rv">
        <img class="ph" src="/herradura/img/tiago.jpg" alt="Tiago Leao" width="264" height="264" loading="lazy" decoding="async">
        <div>
          <img class="logo" src="/herradura/img/logo-sbt.png" alt="soldbytiago Real Estate Group" width="900" height="201" loading="lazy">
          <h3>Tiago Leao</h3>
          <p class="role">[[a1_role]]</p>
          <p class="firm">[[a1_firm]]</p>
          <p class="bio">[[a1_p]]</p>
          <div class="contact">
            <a href="tel:+{{PHONE}}">{{PHONE_PRETTY}}</a>
            <a href="mailto:{{EMAIL}}">{{EMAIL}}</a>
          </div>
          <div class="actions">
            <a class="btn btn-green" href="{{WA_PACKAGE}}" target="_blank" rel="noopener">[[wa]]</a>
            <a class="btn btn-ghost" href="{{MAILTO}}">[[email]]</a>
          </div>
        </div>
      </article>
      <article class="agent rv d1">
        <img class="ph" src="/herradura/img/gabriel.jpg" alt="Gabriel Sáenz" width="264" height="264" loading="lazy" decoding="async">
        <div>
          <img class="logo lok" src="/herradura/img/logo-lokation.png" alt="LoKation Real Estate" width="812" height="149" loading="lazy">
          <h3>Gabriel Sáenz</h3>
          <p class="role">[[a2_role]]</p>
          <p class="firm">[[a2_firm]]</p>
          <p class="bio">[[a2_p]]</p>
          <div class="contact">
            <a href="tel:+19545957719">+1 (954) 595-7719</a>
          </div>
          <div class="actions">
            <a class="btn btn-green" href="tel:+19545957719">[[call]]</a>
          </div>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="cta" id="contact">
  <img src="/herradura/img/g/ocean-dusk.jpg" alt="" loading="lazy" decoding="async" width="1280" height="960">
  <div class="wrap">
    <p class="kicker rv">[[ct_kicker]]</p>
    <h2 class="rv d1">[[ct_h2]]<span class="sq" aria-hidden="true"></span></h2>
    <p class="rv d2">[[ct_p]]</p>
    <div class="cta-btns rv d2">
      <a class="btn btn-white" href="{{WA_VISIT}}" target="_blank" rel="noopener">[[ct_b1]]</a>
      <a class="btn btn-line" href="{{MAILTO}}">[[ct_b2]]</a>
    </div>
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    <div class="brands">
      <img src="/herradura/img/logo-sbt-light.png" alt="soldbytiago Real Estate Group" width="900" height="201" loading="lazy">
      <i aria-hidden="true"></i>
      <img class="lok" src="/herradura/img/logo-lokation-light.png" alt="LoKation Real Estate" width="812" height="149" loading="lazy">
    </div>
    <p class="addr">[[ft_addr]]</p>
    <p>Tiago Leao · Gabriel Sáenz · <a href="https://soldbytiago.com/">soldbytiago.com</a></p>
    <p class="fine">[[ft_fine]]</p>
  </div>
</footer>

<a class="wa-float" href="{{WA_PACKAGE}}" target="_blank" rel="noopener" aria-label="[[wa_float]]">
  <svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16.04 3C9.16 3 3.57 8.59 3.57 15.47c0 2.2.58 4.35 1.68 6.25L3.5 28.5l6.94-1.82a12.4 12.4 0 0 0 5.6 1.34h.01c6.88 0 12.47-5.59 12.47-12.47 0-3.33-1.3-6.46-3.65-8.82A12.39 12.39 0 0 0 16.04 3zm0 22.92h-.01a10.4 10.4 0 0 1-5.3-1.45l-.38-.23-3.94 1.03 1.05-3.84-.25-.4a10.37 10.37 0 0 1-1.59-5.56c0-5.73 4.66-10.39 10.4-10.39 2.78 0 5.39 1.08 7.35 3.05a10.33 10.33 0 0 1 3.04 7.35c0 5.73-4.66 10.4-10.37 10.4zm5.7-7.78c-.31-.16-1.85-.91-2.13-1.02-.29-.1-.5-.16-.7.16-.21.31-.81 1.02-.99 1.23-.18.2-.36.23-.68.08-.31-.16-1.32-.49-2.5-1.55-.93-.83-1.55-1.85-1.74-2.16-.18-.31-.02-.48.14-.64.14-.14.31-.36.47-.55.16-.18.21-.31.31-.52.1-.2.05-.39-.03-.55-.08-.16-.7-1.7-.96-2.32-.25-.61-.51-.53-.7-.54l-.6-.01c-.2 0-.54.08-.82.39-.29.31-1.08 1.06-1.08 2.58 0 1.52 1.1 2.99 1.26 3.2.16.2 2.17 3.32 5.26 4.65.74.32 1.31.51 1.76.65.74.24 1.41.2 1.94.12.59-.09 1.85-.75 2.11-1.48.26-.73.26-1.36.18-1.49-.08-.13-.29-.2-.6-.36z"/></svg>
</a>

<div id="lb" role="dialog" aria-modal="true" aria-label="[[lb_label]]">
  <div class="lb-top">
    <span id="lbCount"></span>
    <button id="lbClose" aria-label="[[lb_close]]"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 5l14 14M19 5L5 19"/></svg></button>
  </div>
  <div class="lb-stage">
    <button class="lb-nav lb-prev" id="lbPrev" aria-label="[[lb_prev]]"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 5l-7 7 7 7"/></svg></button>
    <img id="lbImg" alt="">
    <button class="lb-nav lb-next" id="lbNext" aria-label="[[lb_next]]"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 5l7 7-7 7"/></svg></button>
  </div>
  <p class="lb-cap" id="lbCap"></p>
</div>

<script>
(function(){
  var d=document, root=d.documentElement;
  root.classList.add('js');

  // header
  var hd=d.getElementById('hd');
  function onScroll(){hd.classList.toggle('scrolled', window.scrollY>40)}
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();

  // language switch keeps your place on the page
  d.querySelectorAll('.lang a').forEach(function(a){
    a.addEventListener('click',function(){
      try{
        var max=d.documentElement.scrollHeight-window.innerHeight;
        sessionStorage.setItem('hr_pos', max>0 ? String(window.scrollY/max) : '0');
      }catch(e){}
    });
  });
  try{
    var pos=sessionStorage.getItem('hr_pos');
    if(pos!==null){
      sessionStorage.removeItem('hr_pos');
      var restore=function(){
        var max=d.documentElement.scrollHeight-window.innerHeight;
        root.style.scrollBehavior='auto';
        window.scrollTo(0, parseFloat(pos)*max);
        root.style.scrollBehavior='';
      };
      restore(); window.addEventListener('load',restore);
    }
  }catch(e){}

  // reveal
  var els=d.querySelectorAll('.rv');
  if(typeof IntersectionObserver==='function'){
    var io=new IntersectionObserver(function(en){
      en.forEach(function(e){if(e.isIntersecting){e.target.classList.add('on');io.unobserve(e.target)}});
    },{threshold:.1,rootMargin:'0px 0px -6% 0px'});
    els.forEach(function(e){io.observe(e)});
  }else{els.forEach(function(e){e.classList.add('on')})}

  // lightbox
  var items=[].slice.call(d.querySelectorAll('a[data-lb]')), lb=d.getElementById('lb'),
      img=d.getElementById('lbImg'), cap=d.getElementById('lbCap'), cnt=d.getElementById('lbCount'), cur=0, last=null;
  function show(i){
    cur=(i+items.length)%items.length;
    var a=items[cur]; img.src=a.getAttribute('href'); img.alt=a.dataset.cap||'';
    cap.textContent=a.dataset.cap||''; cnt.textContent=(cur+1)+' / '+items.length;
  }
  function open(i){last=d.activeElement;lb.classList.add('open');d.body.style.overflow='hidden';show(i);d.getElementById('lbClose').focus()}
  function close(){lb.classList.remove('open');d.body.style.overflow='';img.removeAttribute('src');if(last)last.focus()}
  items.forEach(function(a,i){a.addEventListener('click',function(e){e.preventDefault();open(i)})});
  d.getElementById('lbClose').onclick=close;
  d.getElementById('lbPrev').onclick=function(){show(cur-1)};
  d.getElementById('lbNext').onclick=function(){show(cur+1)};
  lb.addEventListener('click',function(e){if(e.target===lb||e.target.classList.contains('lb-stage'))close()});
  d.addEventListener('keydown',function(e){
    if(!lb.classList.contains('open'))return;
    if(e.key==='Escape')close(); else if(e.key==='ArrowLeft')show(cur-1); else if(e.key==='ArrowRight')show(cur+1);
  });
  var sx=null;
  lb.addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});
  lb.addEventListener('touchend',function(e){
    if(sx===null)return; var dx=e.changedTouches[0].clientX-sx; sx=null;
    if(Math.abs(dx)>50)show(cur+(dx<0?1:-1));
  },{passive:true});

  // map: loaded only when the section is near the viewport
  var mapEl=d.getElementById('map'), started=false;
  var PLACES={{PLACES}};
  function initMap(){
    if(typeof mapboxgl==='undefined')return;
    mapboxgl.accessToken='{{MAPBOX_TOKEN}}';
    var map=new mapboxgl.Map({
      container:mapEl, style:'mapbox://styles/mapbox/satellite-streets-v12',
      center:[-84.645,9.642], zoom:11.6, attributionControl:false, cooperativeGestures:true
    });
    map.addControl(new mapboxgl.AttributionControl({compact:true}));
    map.addControl(new mapboxgl.NavigationControl({showCompass:false}),'top-right');
    var b=new mapboxgl.LngLatBounds();
    PLACES.forEach(function(p){
      var el=d.createElement('div'); el.className='mk'+(p.prop?' prop':'')+(p.left?' left':'');
      el.innerHTML='<i></i><span></span>'; el.lastChild.textContent=p.name;
      new mapboxgl.Marker({element:el,anchor:p.left?'right':'left',offset:[p.prop?-10:(p.left?6:-6),0]}).setLngLat(p.at).addTo(map);
      b.extend(p.at);
    });
    var small=mapEl.clientWidth<560;
    map.fitBounds(b,{padding:{top:60,bottom:60,left:small?40:70,right:small?130:190},duration:0});
  }
  function loadMap(){
    if(started)return; started=true;
    var l=d.createElement('link'); l.rel='stylesheet'; l.href='https://api.mapbox.com/mapbox-gl-js/v3.3.0/mapbox-gl.css'; d.head.appendChild(l);
    var s=d.createElement('script'); s.src='https://api.mapbox.com/mapbox-gl-js/v3.3.0/mapbox-gl.js'; s.onload=initMap; d.head.appendChild(s);
  }
  if(mapEl){
    if(typeof IntersectionObserver==='function'){
      var mo=new IntersectionObserver(function(en){if(en[0].isIntersecting){mo.disconnect();loadMap()}},{rootMargin:'600px 0px'});
      mo.observe(mapEl);
    }else{loadMap()}
  }
})();
</script>
</body>
</html>
"""


def render(i):
    t = lambda k: T[k][i]
    e = lambda s: html.escape(s, quote=True)
    wa = lambda key: "https://wa.me/%s?text=%s" % (PHONE, quote(t(key)))
    gal = []
    for n, (f, cap, big) in enumerate(GALLERY):
        cls = ' class="big"' if n == 0 else (' class="big big2"' if big else "")
        gal.append(
            '      <a href="/herradura/img/g/%s.jpg"%s data-lb data-cap="%s"><img src="/herradura/img/g/%s.jpg" alt="%s" loading="lazy" decoding="async"><span>%s</span></a>'
            % (f, cls, e(t(cap)), f if big else f + "-t", e(t(cap)), e(t(cap))))
    places = [
        {"name": t("mk_prop"), "at": [-84.635001, 9.661042], "prop": True},
        {"name": t("mk_plaza"), "at": [-84.6390, 9.6609], "left": True},
        {"name": t("mk_ls"), "at": [-84.6647, 9.6500]},
        {"name": t("mk_jaco"), "at": [-84.6290, 9.6151]},
    ]
    ld = {
        "@context": "https://schema.org", "@type": "RealEstateListing",
        "name": t("ld_name"), "description": t("desc"), "url": t("url"), "inLanguage": t("lang"),
        "image": BASE + "img/hero.jpg",
        "offers": {"@type": "Offer", "price": 16500000, "priceCurrency": "USD", "availability": "https://schema.org/InStock"},
        "about": {
            "@type": "Place", "name": "Finca Herradura",
            "address": {"@type": "PostalAddress", "addressLocality": "Herradura", "addressRegion": "Puntarenas", "addressCountry": "CR"},
            "geo": {"@type": "GeoCoordinates", "latitude": 9.661042, "longitude": -84.635001},
            "additionalProperty": [
                {"@type": "PropertyValue", "name": "Land area", "value": 825380.70, "unitCode": "MTK"},
                {"@type": "PropertyValue", "name": "Land use", "value": "Residential and commercial"},
            ],
        },
        "provider": {"@type": "RealEstateAgent", "name": "Tiago Leao", "url": "https://soldbytiago.com/", "telephone": "+" + PHONE, "email": EMAIL},
    }
    subs = {
        "BASE": BASE, "PRICE": PRICE, "PHONE": PHONE, "PHONE_PRETTY": PHONE_PRETTY, "EMAIL": EMAIL, "MAPS": MAPS,
        "MAPBOX_TOKEN": MAPBOX_TOKEN,
        "WA_PACKAGE": e(wa("wa_msg")), "WA_VISIT": e(wa("wa_visit")),
        "MAILTO": "mailto:%s?subject=%s" % (EMAIL, quote(t("mail_subj"))),
        "CUR_EN": ' aria-current="true"' if i == 0 else "", "CUR_ES": ' aria-current="true"' if i == 1 else "",
        "GALLERY": "\n".join(gal),
        "PLACES": json.dumps(places, ensure_ascii=False),
        "JSONLD": json.dumps(ld, ensure_ascii=False, indent=2),
    }
    out = re.sub(r"\{\{(\w+)\}\}", lambda m: subs[m.group(1)], TEMPLATE)
    out = re.sub(r"\[\[(\w+)\]\]", lambda m: e(t(m.group(1))), out)
    return out


def main():
    for k, v in T.items():
        assert len(v) == 2 and all(v), k
        assert "—" not in v[0] + v[1], "no em dashes in copy: " + k
    for i, rel in enumerate(("herradura/index.html", "herradura/es/index.html")):
        path = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        page = render(i)
        left = re.findall(r"\[\[\w+\]\]|\{\{\w+\}\}", page)
        assert not left, left
        with open(path, "w", encoding="utf-8") as f:
            f.write(page)
        print("wrote", rel, len(page) // 1024, "KB")


if __name__ == "__main__":
    main()
