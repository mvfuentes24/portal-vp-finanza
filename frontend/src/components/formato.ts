const numero = new Intl.NumberFormat("es-VE", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

export const monto = (valor: string | number) => numero.format(Number(valor));

export const fecha = (iso: string) => {
  // Las fechas sin hora (AAAA-MM-DD) se muestran tal cual, sin conversión de zona horaria
  const [a, m, d] = iso.slice(0, 10).split("-");
  return `${d}/${m}/${a}`;
};

/** "1 colaborador", "3 colaboradores" */
export const plural = (n: number, singular: string, varios: string) => `${n} ${n === 1 ? singular : varios}`;

export const fechaHora = (iso: string) =>
  new Date(iso).toLocaleString("es-VE", { dateStyle: "short", timeStyle: "short" });
