import { COLORS } from "@/constants/colors";

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  startIndex: number;
  endIndex: number;
  totalItems: number;
}

export const Pagination = ({
  currentPage,
  totalPages,
  onPageChange,
  startIndex,
  endIndex,
  totalItems,
}: PaginationProps) => {
  if (totalPages <= 1) return null;

  const getPageNumbers = () => {
    const pages: (number | string)[] = [];

    if (totalPages <= 7) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      pages.push(1);
      if (currentPage > 3) pages.push("...");

      const startPage = Math.max(2, currentPage - 1);
      const endPage = Math.min(totalPages - 1, currentPage + 1);

      for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
      }

      if (currentPage < totalPages - 2) pages.push("...");
      pages.push(totalPages);
    }

    return pages;
  };

  return (
    <div className="mt-10 flex flex-col items-center gap-6">
      {/* Información de resultados */}
      <p className={`text-sm ${COLORS.text.secondary}`}>
        Mostrando <span className="text-cyan-400 font-semibold">{startIndex}</span> a{" "}
        <span className="text-cyan-400 font-semibold">{endIndex}</span> de{" "}
        <span className="text-violet-400 font-semibold">{totalItems}</span> resultados
      </p>

      {/* Botones de paginación */}
      <div className="flex items-center gap-2 flex-wrap justify-center">
        {/* Botón Anterior */}
        <button
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
          className={`px-4 py-2 rounded-lg font-medium transition-all ${
            currentPage === 1
              ? `${COLORS.bg.tertiary} ${COLORS.text.tertiary} cursor-not-allowed opacity-50`
              : `${COLORS.bg.secondary} ${COLORS.text.primary} border ${COLORS.border.light} hover:border-cyan-400 hover:text-cyan-400`
          }`}
          aria-label="Página anterior"
        >
          ← Anterior
        </button>

        {/* Números de página */}
        {getPageNumbers().map((page, idx) =>
          page === "..." ? (
            <span key={`dots-${idx}`} className={`px-3 py-2 ${COLORS.text.tertiary}`}>
              ...
            </span>
          ) : (
            <button
              key={page}
              onClick={() => onPageChange(Number(page))}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                currentPage === page
                  ? "bg-gradient-to-r from-cyan-500 to-violet-500 text-white shadow-lg shadow-cyan-500/50"
                  : `${COLORS.bg.secondary} ${COLORS.text.primary} border ${COLORS.border.light} hover:border-cyan-400 hover:text-cyan-400`
              }`}
            >
              {page}
            </button>
          )
        )}

        {/* Botón Siguiente */}
        <button
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
          className={`px-4 py-2 rounded-lg font-medium transition-all ${
            currentPage === totalPages
              ? `${COLORS.bg.tertiary} ${COLORS.text.tertiary} cursor-not-allowed opacity-50`
              : `${COLORS.bg.secondary} ${COLORS.text.primary} border ${COLORS.border.light} hover:border-cyan-400 hover:text-cyan-400`
          }`}
          aria-label="Página siguiente"
        >
          Siguiente →
        </button>
      </div>
    </div>
  );
};
