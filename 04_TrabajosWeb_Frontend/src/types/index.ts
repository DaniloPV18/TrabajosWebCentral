export interface Vacante {
  id: number;
  titulo: string;
  empresa: string;
  ubicacion: string;
  modalidad: "Presencial" | "Remoto" | "Híbrido";
  tipoContrato: "Tiempo Completo" | "Medio Tiempo" | "Contrato";
  area: string;
  descripcion: string;
  requisitos: string[];
  salario?: string;
  fechaPublicacion: string;
  url: string;
  identificador: string;
}

export interface Filtros {
  empresa: string;
  ubicacion: string;
  modalidad: string;
  area: string;
}

export interface ContadorPorEmpresa {
  [key: string]: number;
}
