---
title: About
layout: about
permalink: /about.html
credits: true
---

<style>
.about-layout {
  display: flex;
  gap: 0;
  align-items: stretch;
  min-height: 380px;
  margin-bottom: 3rem;
}
.about-image {
  flex: 0 0 35%;
  position: relative;
  overflow: hidden;
}
.about-image img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
}
.about-image-overlay {
  position: absolute;
  inset: 0;
  background: rgba(12,24,16,0.81);
}
.about-image-caption {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 1rem
}
.about-image-caption h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: .5rem;
  text-align: center;
}
.about-image-caption p {
  font-size: 1rem;
  color: rgba(255,255,255,0.75);
  margin-bottom: 1rem;
  line-height: 1.5;
  padding: 2rem;
}
.btn-project-link {
  background: #477d49;
  color: #fff;
  border-radius: 999px;
  padding: .45rem 1.1rem;
  font-size: .90rem;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: .4rem;
  transition: background .15s;
}
.btn-project-link:hover { background: #193118; color: #fff; }
.btn-project-link svg { flex-shrink: 0; }
.about-text {
  flex: 1;
  padding: 3rem 3.5rem;
  background: #fff;
}
.about-text h2 {
  font-size: 1.35rem;
  font-weight: 700;
  color: #1a2e22;
  margin-bottom: 1.2rem;
  padding-bottom: .4rem;
  border-bottom: 2px solid #d8e8d4;
}
.about-text p {
  text-align: justify;
  color: #333;
  line-height: 1.8;
  margin-bottom: 1.1rem;
  font-size: .97rem;
}
@media (max-width: 768px) {
  .about-layout { flex-direction: column; }
  .about-image { flex: 0 0 280px; min-height: 280px; position: relative; }
  .about-text { padding: 2rem 1.5rem; }
}
</style>

<div class="about-layout">

  <div class="about-image">
    <img src="{{ "/objects/La_Vanguardia_09-09-1944_page-2_cropped.jpg" | relative_url }}" alt="GRESEL-UNED">
    <div class="about-image-overlay"></div>
    <div class="about-image-caption">
      <h1>GRESEL-UNED</h1>
      <p>Repositorio de prensa histórica digitalizada y transcrita de Asia, España y el Caribe hispánico.</p>
      <a class="btn-project-link" href="https://gresel-uned.hypotheses.org/" target="_blank" rel="noopener">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16"><path d="M6.354 5.5H4a3 3 0 0 0 0 6h3a3 3 0 0 0 2.83-4H9q-.13 0-.25.02a2 2 0 0 1-1.786 2.98H4a2 2 0 1 1 0-4h1.535c.218-.376.495-.714.82-1z"/><path d="M9 5a3 3 0 0 0 0 6h3a3 3 0 0 0 0-6zm.184 2.368A2 2 0 0 1 12 6h-3a2 2 0 0 1 .184 4H9a2 2 0 0 1-.816-3.632z"/></svg>
        Visita la web del proyecto
      </a>
    </div>
  </div>

  <div class="about-text">
    <h2>Sobre el repositorio</h2>
    <p>Este repositorio contiene el desarrollo de una plataforma digital para la consulta de prensa histórica dentro del marco del proyecto GRESEL-UNED, construida a partir de la plantilla de CollectionBuilder.</p>
    <p>El objetivo del proyecto es integrar imágenes digitalizadas de periódicos con sus transcripciones generadas mediante OCR, permitiendo una exploración más accesible e interactiva del contenido. Para ello, se ha personalizado la interfaz mediante HTML y se ha incorporado OpenSeadragon como visor, lo que permite visualizar las páginas en alta resolución y superponer regiones que delimitan los distintos artículos.</p>
    <p>Estas regiones han sido anotadas previamente en Transkribus y transformadas de XML a JSON mediante un script en Python, de forma que puedan ser utilizadas en la web. Cada región está conectada con su transcripción, lo que permite al usuario seleccionar una zona concreta de la página y consultar directamente su contenido textual.</p>
    <p>Además, se ha implementado un sistema de búsqueda basado en las transcripciones. Para ello, el texto se extrae y se procesa para reconstruir palabras y párrafos afectados por el formato en columnas, generando archivos que permiten localizar términos dentro del corpus.</p>
    <p>El repositorio se organiza por periódicos y fechas de publicación, combinando imágenes, datos estructurados y metadatos en un mismo entorno. En conjunto, la plataforma facilita la navegación, la consulta y el análisis de la prensa histórica mediante herramientas de código abierto y de bajo coste de mantenimiento.</p>
  </div>

</div>