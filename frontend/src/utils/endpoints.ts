const BASE_URL = "http://localhost:8000";

export interface EndpointType {
  getAll: (skip: number, limit: number) => string;
  getById: (id: string) => string;
  create: string;
  update: (id: string) => string;
  delete: (id: string) => string;
}

interface EndpointsType {
  data_source: EndpointType;
  data_source_type: EndpointType;
  data_source_columns: EndpointType;
}

export const endpoints: EndpointsType = {
  data_source: {
    getAll: (skip: number, limit: number) =>
      `${BASE_URL}/data-sources/all?skip=${skip}&limit=${limit}`,
    getById: (id: string) => `${BASE_URL}/data-sources/?id=${id}`,
    create: `${BASE_URL}/data-sources`,
    update: (id: string) => `${BASE_URL}/data-sources/?id=${id}`,
    delete: (id: string) => `${BASE_URL}/data-sources/?id=${id}`,
  },
  data_source_type: {
    getAll: (skip: number, limit: number) =>
      `${BASE_URL}/data-source-type/all?skip=${skip}&limit=${limit}`,
    getById: (id: string) => `${BASE_URL}/data-source-type/${id}`,
    create: `${BASE_URL}/data-source-type`,
    update: (id: string) => `${BASE_URL}/data-source-type/?id=${id}`,
    delete: (id: string) => `${BASE_URL}/data-source-type/?id=${id}`,
  },
  data_source_columns: {
    getAll: (skip: number, limit: number) =>
      `${BASE_URL}/data-source-columns/all?skip=${skip}&limit=${limit}`,
    getById: (id: string) => `${BASE_URL}/data-source-columns/?id=${id}`,
    create: `${BASE_URL}/data-source-columns`,
    update: (id: string) => `${BASE_URL}/data-source-columns/?id=${id}`,
    delete: (id: string) => `${BASE_URL}/data-source-columns/?id=${id}`,
  },
};
