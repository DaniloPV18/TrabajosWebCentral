// Paleta de colores profesional oscura
export const COLORS = {
  // Fondos
  bg: {
    primary: "bg-[#0f172a]",      // Azul oscuro principal
    secondary: "bg-[#1e293b]",    // Azul-gris secundario
    tertiary: "bg-[#334155]",     // Azul-gris terciario
    accent: "bg-[#06b6d4]/10",    // Cyan con transparencia
  },
  
  // Textos
  text: {
    primary: "text-[#f1f5f9]",    // Blanco frío
    secondary: "text-[#cbd5e1]",  // Gris claro
    tertiary: "text-[#94a3b8]",   // Gris medio
  },
  
  // Bordes
  border: {
    light: "border-[#475569]",
    dark: "border-[#1e293b]",
  },
  
  // Acentos principales
  accent: {
    primary: "bg-[#06b6d4] text-[#0f172a]",      // Cyan
    secondary: "bg-[#8b5cf6] text-white",        // Púrpura
    tertiary: "bg-[#ec4899] text-white",         // Rosa magenta
  },
};

// Colores según modalidad (con nueva paleta oscura)
export const MODALIDAD_COLORS = {
  Remoto: "bg-emerald-500/20 text-emerald-300 border border-emerald-500/50",
  Presencial: "bg-cyan-500/20 text-cyan-300 border border-cyan-500/50",
  Híbrido: "bg-violet-500/20 text-violet-300 border border-violet-500/50",
} as const;

export const TIPO_CONTRATO_COLOR = "bg-slate-700 text-slate-200";
export const AREA_COLOR = "bg-orange-500/20 text-orange-300 border border-orange-500/50";

// Colores hover para elementos interactivos
export const HOVER = {
  primary: "hover:bg-[#06b6d4]/20 hover:text-[#06b6d4]",
  secondary: "hover:bg-[#8b5cf6]/20 hover:text-[#8b5cf6]",
  subtle: "hover:bg-[#334155]",
};

