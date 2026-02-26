import { Vacante } from "@/types";
import { VacanteCard } from "./VacanteCard";
import { EmptyState } from "./EmptyState";
import { Pagination } from "./Pagination";
import { usePaginatedVacantes } from "@/hooks/usePaginatedVacantes";
import { LABELS } from "@/constants/labels";
import { COLORS } from "@/constants/colors";
import { useEffect } from "react";

interface VacanteListProps {
  vacantes: Vacante[];
  totalVacantes: number;
  onLimpiarFiltros: () => void;
}

export const VacanteList = ({
  vacantes,
  totalVacantes,
  onLimpiarFiltros,
}: VacanteListProps) => {
  const pagination = usePaginatedVacantes(vacantes);

  useEffect(() => {
    // reset to first page when the source vacantes change (filters/search)
    pagination.resetPagination();
  }, [vacantes]);
  
  return (
    <div className="lg:col-span-3">
      {/* Resultados Info */}
      <div className="mb-8 p-5 rounded-lg bg-gradient-to-r from-slate-700/30 to-slate-600/20 border border-slate-600 shadow-lg">
        <p className={`${COLORS.text.secondary} font-medium`} role="status">
          {LABELS.MOSTRANDO} <span className="text-cyan-400 font-semibold">{pagination.startIndex}</span> - <span className="text-cyan-400 font-semibold">{pagination.endIndex}</span> {LABELS.DE} <span className={`${COLORS.text.primary} font-bold`}>{pagination.totalItems}</span> {LABELS.VACANTES}
        </p>
      </div>

      {totalVacantes > 0 ? (
        <div className="space-y-4">
          {pagination.vacantesPaginadas.map((vacante) => (
            <VacanteCard key={vacante.id} vacante={vacante} />
          ))}
        </div>
      ) : (
        <EmptyState onLimpiarFiltros={onLimpiarFiltros} />
      )}
      
      {totalVacantes > 0 && (
        <Pagination
          currentPage={pagination.paginaActual}
          totalPages={pagination.totalPages}
          onPageChange={pagination.goToPage}
          startIndex={pagination.startIndex}
          endIndex={pagination.endIndex}
          totalItems={pagination.totalItems}
        />
      )}
    </div>
  );
};
