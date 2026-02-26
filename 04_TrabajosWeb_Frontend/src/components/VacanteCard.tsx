import { useState } from "react";
import { Vacante } from "@/types";
import { LABELS, ARIA_LABELS } from "@/constants/labels";
import { MODALIDAD_COLORS, TIPO_CONTRATO_COLOR, AREA_COLOR, COLORS } from "@/constants/colors";
import { formatFecha } from "@/lib/utils";

interface VacanteCardProps {
  vacante: Vacante;
}

export const VacanteCard = ({ vacante }: VacanteCardProps) => {
  const [expandido, setExpandido] = useState(false);

  const getModalidadColor = (modalidad: string) => {
    return (
      MODALIDAD_COLORS[modalidad as keyof typeof MODALIDAD_COLORS] ||
      "bg-slate-700 text-slate-300"
    );
  };

  const toggleExpand = () => setExpandido(!expandido);

  return (
    <article
        className={`${COLORS.bg.secondary} rounded-xl hover:shadow-2xl transition-all border ${COLORS.border.light} hover:border-cyan-500/50 hover:bg-opacity-80 overflow-hidden group`}
      role="article"
      aria-label={`Vacante: ${vacante.titulo}`}
    >
        {/* Top border con gradiente */}
        <div className="h-1 bg-gradient-to-r from-cyan-500 to-violet-500"></div>
      
      <div className="p-6 cursor-pointer hover:bg-slate-700/30" onClick={toggleExpand}>
        <div className="flex items-start justify-between gap-4 mb-3">
          <div className="flex-1 min-w-0">
              <h3 className={`text-xl font-bold ${COLORS.text.primary} mb-2 truncate group-hover:text-cyan-400 transition-colors`}>
              {vacante.titulo}
            </h3>
            <div className="flex flex-wrap gap-2">
              <span
                className={`text-xs font-semibold px-3 py-1 rounded-lg ${getModalidadColor(
                  vacante.modalidad
                )}`}
              >
                {vacante.modalidad}
              </span>
              <span className={`text-xs font-semibold px-3 py-1 rounded-lg ${TIPO_CONTRATO_COLOR}`}>
                {vacante.tipoContrato}
              </span>
              <span className={`text-xs font-semibold px-3 py-1 rounded-lg ${AREA_COLOR}`}>
                {vacante.area}
              </span>
            </div>
          </div>
          <button
            onClick={(e) => {
              e.stopPropagation();
              toggleExpand();
            }}
            aria-label={ARIA_LABELS.EXPAND_DETAILS}
            aria-expanded={expandido}
            className={`text-2xl flex-shrink-0 ${COLORS.text.tertiary} hover:text-cyan-400 transition-colors`}
          >
            {expandido ? "▼" : "▶"}
          </button>
        </div>

        {/* Información de una línea visible siempre */}
        <div className={`flex items-center gap-4 text-sm ${COLORS.text.secondary} flex-wrap`}>
          <span>📍 {vacante.ubicacion}</span>
          {vacante.salario && <span>💰 {vacante.salario}</span>}
        </div>
      </div>

      {/* Detalles expandibles */}
      {expandido && (
        <div className={`border-t ${COLORS.border.light} px-6 py-4 ${COLORS.bg.tertiary}/50 animate-in fade-in duration-200`}>
          <div className="mb-4">
            <h4 className={`font-semibold ${COLORS.text.primary} mb-2 text-cyan-400`}>
              {LABELS.DESCRIPCION}
            </h4>
            <p className={`text-sm ${COLORS.text.secondary} leading-relaxed`}>
              {vacante.descripcion}
            </p>
          </div>

          {vacante.requisitos.length > 0 && (
            <div className="mb-4">
              <h4 className={`font-semibold ${COLORS.text.primary} mb-2 text-cyan-400`}>
                {LABELS.REQUISITOS}
              </h4>
              <ul className={`list-disc list-inside space-y-1 ${COLORS.text.secondary}`}>
                {vacante.requisitos.map((req, idx) => (
                  <li key={idx} className="text-sm">
                    {req}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pt-4 border-t border-slate-700">
            <time className={`text-xs ${COLORS.text.tertiary}`}>
              {LABELS.PUBLICADO}: {formatFecha(vacante.fechaPublicacion)}
            </time>
            <a
              href={vacante.url}
              target="_blank"
              rel="noopener noreferrer"
              className="px-5 py-2 bg-gradient-to-r from-cyan-500 to-violet-500 text-white rounded-lg hover:from-cyan-600 hover:to-violet-600 transition-all text-sm font-semibold whitespace-nowrap shadow-lg hover:shadow-cyan-500/50"
            >
              {LABELS.VER_VACANTE} →
            </a>
          </div>
        </div>
      )}
    </article>
  );
};
