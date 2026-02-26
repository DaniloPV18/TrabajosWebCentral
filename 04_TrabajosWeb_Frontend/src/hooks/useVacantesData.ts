import { useMemo } from "react";
import { vacantesData, obtenerEmpresas, obtenerUbicaciones, obtenerAreas, obtenerModalidades, obtenerContadorPorEmpresa } from "@/data/vacantes";

export const useVacantesData = () => {
  const empresas = useMemo(() => obtenerEmpresas(), []);
  const ubicaciones = useMemo(() => obtenerUbicaciones(), []);
  const areas = useMemo(() => obtenerAreas(), []);
  const modalidades = useMemo(() => obtenerModalidades(), []);
  const contadorPorEmpresa = useMemo(() => obtenerContadorPorEmpresa(), []);

  return {
    empresas,
    ubicaciones,
    areas,
    modalidades,
    contadorPorEmpresa,
    totalVacantes: vacantesData.length,
  };
};
