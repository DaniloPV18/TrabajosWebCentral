import { useState, useMemo } from "react";
import { Vacante } from "@/types";

const ITEMS_PER_PAGE = 6;

export const usePaginatedVacantes = (vacantes: Vacante[]) => {
  const [paginaActual, setPaginaActual] = useState(1);

  const paginationData = useMemo(() => {
    const totalPages = Math.ceil(vacantes.length / ITEMS_PER_PAGE);
    const startIndex = (paginaActual - 1) * ITEMS_PER_PAGE;
    const endIndex = startIndex + ITEMS_PER_PAGE;
    const vacantesPaginadas = vacantes.slice(startIndex, endIndex);

    return {
      vacantesPaginadas,
      paginaActual,
      totalPages,
      totalItems: vacantes.length,
      startIndex: startIndex + 1,
      endIndex: Math.min(endIndex, vacantes.length),
    };
  }, [vacantes, paginaActual]);

  const goToPage = (page: number) => {
    const totalPages = Math.ceil(vacantes.length / ITEMS_PER_PAGE);
    if (page >= 1 && page <= totalPages) {
      setPaginaActual(page);
      // Scroll to top
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const nextPage = () => {
    const totalPages = Math.ceil(vacantes.length / ITEMS_PER_PAGE);
    if (paginaActual < totalPages) {
      goToPage(paginaActual + 1);
    }
  };

  const prevPage = () => {
    if (paginaActual > 1) {
      goToPage(paginaActual - 1);
    }
  };

  const resetPagination = () => {
    setPaginaActual(1);
  };

  return {
    ...paginationData,
    goToPage,
    nextPage,
    prevPage,
    resetPagination,
  };
};
