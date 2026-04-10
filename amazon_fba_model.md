# MODELO ECONÓMICO AMAZON FBA — ANÁLISIS DE VIABILIDAD
> Versión 1.0 | Estructura lista para Excel / Google Sheets

---

## HOJA 1: INPUTS — VARIABLES EDITABLES

### BLOQUE A — PRODUCTO

| # | Variable | Valor ejemplo | Unidad | Notas |
|---|----------|--------------|--------|-------|
| A1 | Coste unitario producto (EXW/FOB) | 4.50 | EUR | Precio negociado con fábrica |
| A2 | MOQ (cantidad mínima pedido) | 500 | uds | |
| A3 | Coste packaging por unidad | 0.30 | EUR | Caja, bolsa, etiqueta |
| A4 | Coste inspección en origen | 300.00 | EUR (fijo) | Pre-shipment inspection |
| A5 | Coste agente/intermediario | 0.00 | EUR | 0 si tratas directo |

**Coste producto por unidad:**
```
= A1 + A3 + (A4 / A2) + (A5 / A2)
= 4.50 + 0.30 + (300/500) + 0
= 5.40 EUR/ud
```

---

### BLOQUE B — LOGÍSTICA INTERNACIONAL

| # | Variable | Valor ejemplo | Unidad | Notas |
|---|----------|--------------|--------|-------|
| B1 | Método de envío | Marítimo | — | Marítimo / Aéreo / Tren |
| B2 | Peso por unidad | 0.45 | kg | Peso bruto con packaging |
| B3 | Volumen por unidad | 0.002 | m³ | Solo si se factura por volumen |
| B4 | Coste por kg (flete) | 1.20 | EUR/kg | Marítimo ~0.8–1.5, Aéreo ~4–8 |
| B5 | Aranceles aduaneros (%) | 6.70 | % | Sobre valor FOB, depende de HS code |
| B6 | Despacho aduanero (fijo) | 200.00 | EUR | Agente transitario |
| B7 | Seguro de transporte (%) | 0.50 | % | Sobre valor mercancía |
| B8 | Costes portuarios / THC | 150.00 | EUR | Terminal handling charge |
| B9 | Transporte interno (destino) | 180.00 | EUR | Del puerto/aeropuerto a almacén |

**Coste logístico por unidad:**
```
Peso total lote     = B2 × A2 = 0.45 × 500 = 225 kg
Flete total         = B2 × B4 × A2 = 225 × 1.20 = 270 EUR
Valor FOB lote      = A1 × A2 = 4.50 × 500 = 2,250 EUR
Arancel total       = Valor FOB × (B5/100) = 2,250 × 6.70% = 150.75 EUR
Seguro total        = Valor FOB × (B7/100) = 2,250 × 0.50% = 11.25 EUR
Costes fijos total  = B6 + B8 + B9 = 200 + 150 + 180 = 530 EUR

Coste logístico total lote = Flete + Arancel + Seguro + Costes fijos
                           = 270 + 150.75 + 11.25 + 530 = 962 EUR

Coste logístico por unidad = 962 / 500 = 1.924 EUR/ud
```

---

### BLOQUE C — COSTES AMAZON

| # | Variable | Valor ejemplo | Unidad | Notas |
|---|----------|--------------|--------|-------|
| C1 | Precio de venta (PVP) | 24.99 | EUR | Precio final al consumidor |
| C2 | Comisión referencia Amazon (%) | 15.00 | % | Varía por categoría (ver tabla abajo) |
| C3 | Coste FBA por unidad | 3.50 | EUR | Picking, packing, envío Amazon |
| C4 | Almacenamiento mensual por ud | 0.35 | EUR/ud | Basado en volumen y temporada |
| C5 | Tasa devoluciones (%) | 5.00 | % | % de ventas que se devuelven |
| C6 | Coste por devolución | 1.50 | EUR | Tramitación + coste FBA retorno |
| C7 | Coste destrucción/retirada | 0.00 | EUR/ud | Si hay stock caducado o retirado |

**Comisiones de referencia por categoría (referencia 2024–2025):**
| Categoría | Comisión |
|-----------|----------|
| Hogar y jardín | 15% |
| Deportes y aire libre | 15% |
| Electrónica | 8% |
| Juguetes | 15% |
| Salud y belleza | 8–15% |
| Ropa y moda | 17% |
| Alimentación | 8% |
| Libros | 15% |

**Coste Amazon por unidad:**
```
Comisión Amazon     = C1 × (C2/100) = 24.99 × 15% = 3.749 EUR
Coste devolución    = C1 × (C5/100) × C6 = 24.99 × 5% × 1.50 = 0.075 EUR → simplificado: (C5/100) × C6
Coste Amazon/ud     = Comisión + FBA + Almacenamiento + Coste devolución
                    = 3.749 + 3.50 + 0.35 + 0.075 = 7.674 EUR/ud
```

---

### BLOQUE D — MARKETING / PUBLICIDAD

| # | Variable | Valor ejemplo | Unidad | Notas |
|---|----------|--------------|--------|-------|
| D1 | CPC medio (coste por clic) | 0.55 | EUR | Según nicho y competencia |
| D2 | Tasa de conversión (%) | 12.00 | % | 8–15% es rango típico |
| D3 | ACOS objetivo (%) | 20.00 | % | Advertising Cost of Sales |
| D4 | Presupuesto diario PPC | 15.00 | EUR | |

**Coste publicitario por unidad vendida:**
```
Clics necesarios por venta = 1 / (D2/100) = 1 / 12% = 8.33 clics
Coste ads por venta        = D1 × Clics = 0.55 × 8.33 = 4.58 EUR/ud

Verificación ACOS:
ACOS real = Coste ads / PVP = 4.58 / 24.99 = 18.3%  ← debe ser ≤ D3

Ventas diarias estimadas (del presupuesto):
Clics/día = D4 / D1 = 15 / 0.55 = 27.3 clics/día
Ventas/día = Clics × Conversión = 27.3 × 12% = 3.27 uds/día
```

---

### BLOQUE E — FISCALIDAD Y FINANCIACIÓN

| # | Variable | Valor ejemplo | Unidad | Notas |
|---|----------|--------------|--------|-------|
| E1 | IVA (ingresos) | 21.00 | % | Aplica si vendes como empresa |
| E2 | Tipo impositivo IS/IRPF | 25.00 | % | Para calcular beneficio neto real |
| E3 | Costes financieros (%) | 0.00 | % | Si financies con crédito |

> **Nota:** El PVP en Amazon suele ser IVA incluido. Amazon te ingresa el PVP sin IVA si eres empresa registrada. Calcula siempre sobre precio neto de IVA.

```
PVP neto (sin IVA) = C1 / (1 + E1/100) = 24.99 / 1.21 = 20.65 EUR
```

---

## HOJA 2: OUTPUTS — CÁLCULOS AUTOMÁTICOS

### RESUMEN DE COSTES POR UNIDAD

| Concepto | Fórmula | Valor (EUR) |
|----------|---------|-------------|
| Coste producto | A1 + A3 + (A4/A2) + (A5/A2) | 5.40 |
| Coste logístico | (Flete+Arancel+Seguro+Fijos)/A2 | 1.92 |
| Coste Amazon | Comisión + FBA + Almacen + Devoluc | 7.67 |
| Coste publicidad | CPC / Conversión | 4.58 |
| **COSTE TOTAL LANDED** | Suma de todos | **19.57** |

---

### MÁRGENES Y RENTABILIDAD

| KPI | Fórmula Excel | Valor |
|-----|--------------|-------|
| PVP neto (sin IVA) | =C1/(1+E1/100) | 20.65 EUR |
| Coste total por unidad | =SUMA(costes) | 19.57 EUR |
| **Beneficio bruto/ud** | =PVP_neto - Coste_total | **1.08 EUR** |
| **Margen neto (%)** | =Beneficio/PVP_neto×100 | **5.23%** |
| Beneficio antes impuestos | =Beneficio_bruto | 1.08 EUR |
| Impuesto estimado (25%) | =Beneficio × E2/100 | 0.27 EUR |
| **Beneficio neto real/ud** | =Beneficio - Impuesto | **0.81 EUR** |

> **ALERTA:** Un margen neto del 5% es peligroso. El mínimo recomendado es 20–25%.

---

### ANÁLISIS DEL PEDIDO INICIAL (MOQ)

| KPI | Fórmula | Valor |
|-----|---------|-------|
| Inversión total en stock | =(A1+A3)×A2 + Logística_total | 3,662 EUR |
| Ingresos totales (venta 100%) | =C1_neto × A2 | 10,325 EUR |
| Beneficio total lote (bruto) | =Beneficio_ud × A2 | 540 EUR |
| **ROI sobre inversión** | =Beneficio_total/Inversión×100 | **14.7%** |
| Tiempo estimado retorno | MOQ/Ventas_dia | ~153 días |

---

### PUNTO DE EQUILIBRIO (BREAK-EVEN)

```
Break-even en unidades = Costes fijos totales / Margen contribución por unidad

Costes fijos (por lote):
  - Inspección origen:    300 EUR
  - Despacho aduanas:     200 EUR
  - Costes portuarios:    150 EUR
  - Transporte interno:   180 EUR
  Total costes fijos:     830 EUR

Margen contribución/ud = PVP_neto - Costes_variables_ud
  = 20.65 - (5.40 + 1.92 + 7.67 + 4.58) → solo variables
  = 20.65 - 19.57 = 1.08 EUR/ud

Break-even (uds) = 830 / 1.08 = 769 unidades  ← SUPERA el MOQ de 500!

Con MOQ de 500 uds, necesitarías un PVP más alto o menores costes.
```

---

## HOJA 3: ESCENARIOS

### TABLA DE ESCENARIOS COMPARATIVOS

| Variable | Pesimista | Realista | Optimista |
|----------|-----------|----------|-----------|
| Precio venta (PVP) | 21.99 EUR | 24.99 EUR | 27.99 EUR |
| CPC medio | 0.75 EUR | 0.55 EUR | 0.35 EUR |
| Tasa conversión | 8% | 12% | 16% |
| Coste logístico/ud | 2.50 EUR | 1.92 EUR | 1.50 EUR |
| Tasa devoluciones | 8% | 5% | 3% |

### RESULTADOS POR ESCENARIO

| KPI | Pesimista | Realista | Optimista |
|-----|-----------|----------|-----------|
| PVP neto (sin IVA) | 18.17 EUR | 20.65 EUR | 23.13 EUR |
| Coste publicidad/ud | 9.38 EUR | 4.58 EUR | 2.19 EUR |
| Coste logístico/ud | 2.50 EUR | 1.92 EUR | 1.50 EUR |
| Coste total/ud | 22.02 EUR | 19.57 EUR | 17.33 EUR |
| **Beneficio bruto/ud** | **-3.85 EUR** | **1.08 EUR** | **5.80 EUR** |
| **Margen neto** | **-21.2%** | **5.2%** | **25.1%** |
| Beneficio lote (500 uds) | -1,925 EUR | 540 EUR | 2,900 EUR |
| **Decisión** | **NO LANZAR** | **AJUSTAR** | **LANZAR** |

**Cálculos de coste publicidad por escenario:**
```
Pesimista:  CPC/Conv = 0.75/0.08 = 9.38 EUR/venta
Realista:   CPC/Conv = 0.55/0.12 = 4.58 EUR/venta
Optimista:  CPC/Conv = 0.35/0.16 = 2.19 EUR/venta
```

---

## HOJA 4: ANÁLISIS DE SENSIBILIDAD

### S1 — IMPACTO DEL CPC EN EL BENEFICIO (conversión fija 12%)

| CPC (EUR) | Coste ads/ud | Beneficio/ud | Margen % |
|-----------|-------------|-------------|----------|
| 0.25 | 2.08 | 3.50 | 16.9% |
| 0.35 | 2.92 | 2.66 | 12.9% |
| 0.45 | 3.75 | 1.83 | 8.9% |
| **0.55** | **4.58** | **1.08** | **5.2%** |
| 0.65 | 5.42 | -0.75 | -3.6% |
| 0.75 | 6.25 | -2.17 | -10.5% |
| 0.85 | 7.08 | -3.00 | -14.5% |

> **Umbral CPC crítico:** Con estos costes, el CPC máximo sostenible es ~0.58 EUR (beneficio 0).
> Fórmula: `CPC_max = PVP_neto × ACOS_objetivo_max / (1/Conversión)`

---

### S2 — IMPACTO DEL PRECIO DE VENTA (CPC y costes fijos)

| PVP (EUR) | PVP neto | Beneficio/ud | Margen % | Break-even (uds) |
|-----------|----------|-------------|----------|-----------------|
| 19.99 | 16.52 | -3.05 | -18.5% | Negativo |
| 21.99 | 18.17 | -1.40 | -7.7% | Negativo |
| 23.99 | 19.83 | 0.26 | 1.3% | >3,000 |
| **24.99** | **20.65** | **1.08** | **5.2%** | **769** |
| 26.99 | 22.31 | 2.74 | 12.3% | 303 |
| 28.99 | 23.96 | 4.39 | 18.3% | 189 |
| 31.99 | 26.44 | 6.87 | 26.0% | 121 |

> **PVP mínimo para ser rentable** con estos costes: ~23.60 EUR

---

### S3 — IMPACTO DE LOS COSTES LOGÍSTICOS

| Coste logístico/ud | Beneficio/ud | Margen % | Escenario típico |
|-------------------|-------------|----------|-----------------|
| 1.00 | 1.92 | 9.3% | Marítimo, volumen alto |
| 1.50 | 1.42 | 6.9% | Marítimo favorable |
| **1.92** | **1.08** | **5.2%** | **Base case** |
| 2.50 | 0.50 | 2.4% | Marítimo caro / aéreo económico |
| 3.50 | -0.50 | -2.4% | Aéreo estándar |
| 5.00 | -2.00 | -9.7% | Aéreo urgente |

> **Conclusión:** Para este producto, el aéreo destruye completamente el margen.

---

### S4 — MATRIZ BENEFICIO/UD: CPC × CONVERSIÓN

| CPC \ Conv | 6% | 8% | 10% | 12% | 15% | 18% |
|-----------|----|----|-----|-----|-----|-----|
| 0.25 EUR | -2.08 | 0.67 | 2.15 | 3.50 | 4.33 | 5.72 |
| 0.35 EUR | -3.42 | -0.50 | 1.15 | 2.66 | 3.98 | 5.20 |
| 0.45 EUR | -4.42 | -1.25 | 0.15 | 1.83 | 3.33 | 4.65 |
| 0.55 EUR | -5.75 | -2.42 | -0.85 | 1.08 | 2.74 | 4.15 |
| 0.65 EUR | -6.75 | -3.42 | -1.85 | -0.75 | 1.75 | 3.32 |
| 0.75 EUR | -8.08 | -4.75 | -2.85 | -2.17 | 0.75 | 2.48 |

> Las celdas en positivo son viables. Las negativas destruyen valor.
> En verde: margen >15%. En amarillo: 5–15%. En rojo: <5%.

---

## HOJA 5: MÉTRICAS CLAVE Y SEMÁFORO DE DECISIÓN

### DASHBOARD KPIs

| KPI | Tu modelo | Umbral OK | Umbral Riesgo | Umbral Stop |
|-----|-----------|-----------|--------------|-------------|
| Margen neto % | 5.2% | >20% | 10–20% | <10% |
| ROI por lote | 14.7% | >50% | 25–50% | <25% |
| ACOS real | 22.2% | <20% | 20–30% | >30% |
| Break-even (uds) | 769 | <MOQ/2 | <MOQ | >MOQ |
| Coste total/PVP | 94.8% | <70% | 70–80% | >80% |
| Días para recuperar | 153 | <60 | 60–120 | >120 |

### SEMÁFORO DE DECISIÓN

```
Con los inputs del ejemplo base:

  Margen neto:     5.2%   → ROJO    ← Insuficiente
  ROI:             14.7%  → ROJO    ← Muy bajo
  ACOS:            22.2%  → AMARILLO← Límite
  Break-even:      769 uds → ROJO   ← Supera MOQ
  
  VEREDICTO: NO LANZAR sin ajustes.
  
  Para lanzar necesitas al menos UNA de estas:
  ├── Subir PVP a ≥28 EUR (+12%)
  ├── Bajar coste producto a ≤3.50 EUR (-22%)
  ├── Reducir CPC a ≤0.35 EUR o mejorar conversión a ≥18%
  └── Negociar logística a ≤1.50 EUR/ud
```

---

## HOJA 6: GUÍA PRÁCTICA Y RECOMENDACIONES

### MARGEN MÍNIMO RECOMENDABLE EN AMAZON

```
Regla del 3× (Rule of Three):
  PVP mínimo = Coste landed × 3

  Si tu coste landed = 7.32 EUR (producto + logística)
  PVP mínimo = 7.32 × 3 = 21.96 EUR
  → Esto cubre Amazon (≈33%) + Ads (≈15%) + deja margen neto 18–22%

Fórmula alternativa (cálculo inverso desde ACOS):
  PVP_mínimo = Coste_total / (1 - Comisión% - FBA%/PVP - ACOS%)
```

**Umbrales de referencia para Amazon EU:**

| Concepto | Mínimo | Óptimo | Excelente |
|----------|--------|--------|-----------|
| Margen neto | 15% | 20–25% | >30% |
| ACOS | — | 15–20% | <12% |
| ROI por lote | 30% | 50–80% | >100% |
| Ratio PVP/coste landed | 2.5× | 3× | 4× |

---

### ERRORES TÍPICOS AL CALCULAR COSTES

| # | Error | Impacto | Solución |
|---|-------|---------|----------|
| 1 | Olvidar el IVA en el PVP | Sobreestimas ingresos 21% | Trabaja siempre con PVP sin IVA |
| 2 | No incluir coste de almacenamiento | Pérdidas en stock lento | Añade 0.20–0.60 EUR/ud/mes |
| 3 | Ignorar devoluciones | Pérdida silenciosa 3–10% | Provisiona siempre ≥5% |
| 4 | CPC demasiado optimista | El ACOS se dispara | Valida con herramientas antes de lanzar |
| 5 | No contar el despacho aduanero | Coste fijo de 150–400 EUR | Siempre suma estos costes al lote |
| 6 | Calcular peso teórico, no volumétrico | El transitario factura por volumen | Usa: max(peso real, peso vol) |
| 7 | Olvidar aranceles (HS code) | Pueden ser 0–45% | Verifica código HS antes de sourcing |
| 8 | No contar el tiempo de capital inmovilizado | El dinero tiene coste | Añade coste financiero si tardas >90 días |
| 9 | Ignorar costes de preparación FBA | Etiquetado, prep center | +0.20–0.50 EUR/ud |
| 10 | PPC siempre encendido desde día 1 | Quemas dinero sin reviews | Lanza con presupuesto mínimo hasta 10+ reviews |

---

### INDICADORES CLAVE PARA DECIDIR SI LANZAR

**CHECK PRE-LANZAMIENTO (responde sí/no a cada uno):**

```
VIABILIDAD ECONÓMICA
  [ ] Margen neto proyectado ≥ 20%?
  [ ] ROI por lote ≥ 50%?
  [ ] Break-even < MOQ inicial?
  [ ] PVP es ≥ 3× el coste landed?
  [ ] ACOS sostenible con tu margen (ACOS < Margen bruto%)?

MERCADO Y COMPETENCIA
  [ ] Demanda validada (BSR top 3 < 50,000 en la categoría)?
  [ ] ≥ 3 competidores con >100 reviews vendiendo a tu precio objetivo?
  [ ] No hay monopolio de marca (>1 seller dominante)?
  [ ] Puedes diferenciarte (packaging, bundle, mejora)?

OPERACIONAL
  [ ] Proveedor verificado (muestra recibida y aprobada)?
  [ ] Puedes reposicionar en <45 días para evitar rotura de stock?
  [ ] Tienes liquidez para 2 lotes simultáneos (prevención stockout)?
  [ ] Tienes cuenta Amazon Seller activa y en buen estado?

REGLA: Si responde SÍ a ≥ 8 de 12 → LANZAR
        Si responde SÍ a 5–7 de 12 → AJUSTAR antes de lanzar
        Si responde SÍ a < 5 de 12  → NO LANZAR, buscar otro producto
```

---

### FÓRMULAS EXCEL/SHEETS PARA COPIAR

```excel
// COSTE PRODUCTO POR UNIDAD
=B3+B5+(B6/B4)+(B7/B4)

// COSTE LOGÍSTICO POR UNIDAD (fórmula completa)
=((B10*B9*B4)+(B3_FOB*B4*B12/100)+(B3_FOB*B4*B14/100)+(B15+B16+B17))/B4

// PVP NETO SIN IVA
=C3/(1+(E3/100))

// COMISIÓN AMAZON
=PVP_neto*(C4/100)

// COSTE PUBLICIDAD POR VENTA
=D3/(D4/100)

// COSTE TOTAL POR UNIDAD
=coste_producto+coste_logistica+comision+fba+almacenamiento+devoluciones+ads

// MARGEN NETO %
=(PVP_neto-coste_total)/PVP_neto*100

// BREAK-EVEN EN UNIDADES
=costes_fijos_lote/(PVP_neto-costes_variables_ud)

// ROI POR LOTE
=(beneficio_total_lote/inversion_total_lote)*100

// ACOS REAL
=(coste_ads_ud/PVP_neto)*100

// VENTAS DIARIAS ESTIMADAS
=(D6/D3)*(D4/100)

// BENEFICIO MENSUAL ESTIMADO
=ventas_diarias*30*beneficio_neto_ud
```

---

## APÉNDICE — ESTRUCTURA SUGERIDA PARA GOOGLE SHEETS

```
Pestaña 1: INPUTS         → Todo editable, celdas en amarillo
Pestaña 2: CÁLCULOS       → Fórmulas, no editar manualmente
Pestaña 3: ESCENARIOS     → Tabla de 3 columnas (referencia a INPUTS)
Pestaña 4: SENSIBILIDAD   → Tablas de datos con 2 variables (Data Table)
Pestaña 5: DASHBOARD      → Gráficos y semáforo visual
Pestaña 6: HISTÓRICO      → Registro de lotes anteriores
```

**Convención de colores:**
- Amarillo `#FFF2CC` → Input editable
- Azul `#DDEEFF` → Cálculo automático
- Verde `#D9EAD3` → Resultado positivo / OK
- Rojo `#F4CCCC` → Resultado negativo / STOP
- Naranja `#FCE5CD` → Zona de riesgo / revisar

---

*Modelo creado para análisis de viabilidad Amazon FBA — Importación desde China*
*Actualizar inputs cada vez que cambien condiciones de mercado o logística*
