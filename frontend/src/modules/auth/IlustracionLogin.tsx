import { COLORES } from "../../theme";

/**
 * Ilustración decorativa del inicio de sesión (SVG propio): una versión
 * simplificada de la tabla de alertas del portal, con tipos, detalle y estado.
 */
const FILAS: { tipo: number; estado: "pendiente" | "revisada"; detalle: [number, number] }[] = [
  { tipo: 58, estado: "pendiente", detalle: [112, 70] },
  { tipo: 70, estado: "revisada", detalle: [96, 84] },
  { tipo: 58, estado: "pendiente", detalle: [118, 60] },
  { tipo: 64, estado: "pendiente", detalle: [104, 76] },
  { tipo: 58, estado: "revisada", detalle: [92, 66] },
];

export default function IlustracionLogin() {
  const { azulOscuro, azul, celeste, blanco } = COLORES;
  const alto = 40;
  const inicio = 64;

  return (
    <svg viewBox="0 0 420 300" width="100%" style={{ maxWidth: 420 }} role="presentation" aria-hidden="true">
      {/* Sombra */}
      <ellipse cx="210" cy="284" rx="170" ry="12" fill="#000" opacity="0.18" />

      {/* Tarjeta de la tabla */}
      <rect x="20" y="20" width="380" height="252" rx="14" fill={blanco} />

      {/* Encabezado de la tabla */}
      <path d="M20 34 a14 14 0 0 1 14 -14 h352 a14 14 0 0 1 14 14 v30 h-380 z" fill={celeste} opacity="0.55" />
      {[{ x: 36, w: 14 }, { x: 70, w: 34 }, { x: 150, w: 48 }, { x: 330, w: 42 }].map((c) => (
        <rect key={c.x} x={c.x} y="38" width={c.w} height="9" rx="4.5" fill={azulOscuro} opacity="0.8" />
      ))}

      {/* Filas */}
      {FILAS.map((f, i) => {
        const y = inicio + i * alto;
        const centro = y + alto / 2;
        const pendiente = f.estado === "pendiente";
        return (
          <g key={i}>
            {i > 0 && <line x1="20" y1={y} x2="400" y2={y} stroke={celeste} strokeWidth="1" />}
            {/* Número */}
            <rect x="36" y={centro - 4} width="14" height="8" rx="4" fill={celeste} />
            {/* Etiqueta de tipo (borde) */}
            <rect x="66" y={centro - 9} width={f.tipo} height="18" rx="9" fill="none" stroke={azulOscuro} strokeWidth="1.5" opacity="0.6" />
            <rect x="74" y={centro - 3} width={f.tipo - 16} height="6" rx="3" fill={azulOscuro} opacity="0.45" />
            {/* Detalle en dos líneas */}
            <rect x="150" y={centro - 9} width={f.detalle[0]} height="6" rx="3" fill={celeste} />
            <rect x="150" y={centro + 3} width={f.detalle[1]} height="6" rx="3" fill={celeste} opacity="0.6" />
            {/* Estado */}
            <rect x="318" y={centro - 10} width="68" height="20" rx="10" fill={pendiente ? azul : "#2E7D32"} />
            <rect x="330" y={centro - 3} width="44" height="6" rx="3" fill={blanco} opacity="0.9" />
          </g>
        );
      })}
    </svg>
  );
}
