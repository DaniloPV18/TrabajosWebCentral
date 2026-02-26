import { useMemo } from "react";
import { vacantesData } from "@/data/vacantes";
import { filtrarVacantes } from "@/lib/utils";

export const useFilteredVacantes = (busqueda: string, filtros: any) => {
  const vacantesFiltered = useMemo(() => {
    return filtrarVacantes(vacantesData, busqueda, filtros);
  }, [busqueda, filtros]);

  return vacantesFiltered;
};
