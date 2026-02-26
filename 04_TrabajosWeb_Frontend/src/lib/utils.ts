// Utilidades generales
export const formatFecha = (fecha: string): string => {
  const date = new Date(fecha);
  return date.toLocaleDateString("es-ES", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

export const filtrarVacantes = (
  vacantes: any[],
  busqueda: string,
  filtros: any
) => {
  return vacantes.filter((vacante) => {
    const coincideBusqueda =
      busqueda === "" ||
      vacante.titulo.toLowerCase().includes(busqueda.toLowerCase()) ||
      vacante.empresa.toLowerCase().includes(busqueda.toLowerCase()) ||
      vacante.descripcion.toLowerCase().includes(busqueda.toLowerCase());

    const coincideEmpresa =
      filtros.empresa === "" || vacante.empresa === filtros.empresa;
    const coincideUbicacion =
      filtros.ubicacion === "" || vacante.ubicacion === filtros.ubicacion;
    const coincideModalidad =
      filtros.modalidad === "" || vacante.modalidad === filtros.modalidad;
    const coincideArea = filtros.area === "" || vacante.area === filtros.area;

    return (
      coincideBusqueda &&
      coincideEmpresa &&
      coincideUbicacion &&
      coincideModalidad &&
      coincideArea
    );
  });
};

export const tieneAlgunFiltro = (filtros: any, busqueda: string): boolean => {
  return busqueda !== "" || Object.values(filtros).some((f) => f !== "");
};
