import { LABELS } from "@/constants/labels";
import { COLORS } from "@/constants/colors";

interface EmptyStateProps {
  onLimpiarFiltros: () => void;
}

export const EmptyState = ({ onLimpiarFiltros }: EmptyStateProps) => {
  return (
    <div className={`${COLORS.bg.secondary} rounded-xl shadow-xl p-12 text-center border ${COLORS.border.light}`}>
      <p className="text-6xl mb-6 drop-shadow-lg" aria-hidden="true">
        🔍
      </p>
      <h3 className={`text-2xl font-bold ${COLORS.text.primary} mb-3`}>
        {LABELS.NO_VACANTES}
      </h3>
      <p className={`${COLORS.text.secondary} mb-8 text-lg`}>
        {LABELS.INTENTA_AJUSTAR}
      </p>
      <button
        onClick={onLimpiarFiltros}
        className="px-8 py-3 bg-gradient-to-r from-cyan-500 to-violet-500 text-white rounded-lg hover:from-cyan-600 hover:to-violet-600 transition-all font-semibold shadow-lg hover:shadow-cyan-500/50"
      >
        {LABELS.LIMPIAR} Filtros
      </button>
    </div>
  );
};
