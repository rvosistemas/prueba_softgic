export type Body_login_login_access_token = {
  grant_type?: string | null
  username: string
  password: string
  scope?: string
  client_id?: string | null
  client_secret?: string | null
}

export type HTTPValidationError = {
  detail?: Array<ValidationError>
}

export type ItemCreate = {
  title: string
  description?: string | null
}

export type ItemPublic = {
  title: string
  description?: string | null
  id: string
  owner_id: string
}

export type ItemUpdate = {
  title?: string | null
  description?: string | null
}

export type ItemsPublic = {
  data: Array<ItemPublic>
  count: number
}

export type Message = {
  message: string
}

export type NewPassword = {
  token: string
  new_password: string
}

export type Token = {
  access_token: string
  token_type?: string
}

export type UpdatePassword = {
  current_password: string
  new_password: string
}

export type UserCreate = {
  email: string
  is_active?: boolean
  is_superuser?: boolean
  full_name?: string | null
  password: string
}

export type UserPublic = {
  email: string
  is_active?: boolean
  is_superuser?: boolean
  full_name?: string | null
  id: string
}

export type UserRegister = {
  email: string
  password: string
  full_name?: string | null
}

export type UserUpdate = {
  email?: string | null
  is_active?: boolean
  is_superuser?: boolean
  full_name?: string | null
  password?: string | null
}

export type UserUpdateMe = {
  full_name?: string | null
  email?: string | null
}

export type UsersPublic = {
  data: Array<UserPublic>
  count: number
}

export type ValidationError = {
  loc: Array<string | number>
  msg: string
  type: string
}


export type PlanCreate = {
  nombre: string
  descripcion?: string | null
  activo: boolean
}

export type PlanUpdate = {
  nombre?: string | null
  descripcion?: string | null
  activo?: boolean
}

export type PlanPublic = {
  id: string
  nombre: string
  descripcion?: string | null
  activo: boolean
}

export type PlansPublic = {
  data: Array<PlanPublic>
  count: number
}


export type DetSolicitud = {
  id: string;
  plan: string;
  renovacion: number;
  tipo: string;
  paquete: string;
  fecha_nacimiento: string | null;
  ini_vig_reportada: string;
  fin_vig_reportada: string | null;
  plazo_reportado: number;
  tipo_vig: number;
  sum_aseg_4: number;
  sum_aseg_5: number | null;
  sum_aseg_6: number | null;
  coberturas: Array<any>;
};

export type Cotizacion = {
  id: string;
  plan_comercial: string;
  prima_neta: number;
  iva_notal: number;
  prima_total: number;
  det_solicitudes: Array<DetSolicitud>;
};

export type QuotePublic = {
  id: string;
  response_body: {
    id_convenio: string;
    suc_clave: string;
    suc_nombre: string;
    distribuidor_clave: string;
    distribuidor_nombre: string;
    distribuidor_email: string;
    cotizaciones: Cotizacion[];
  };
  message_error: string | null;
  es_dato_valido: boolean;
};

export type QuotesPublic = {
  data: Array<QuotePublic>;
  hasNextPage: boolean;
};