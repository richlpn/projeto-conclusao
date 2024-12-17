const BASE_URL = "http://localhost:8000";

export const endpoints = {
  data_source: {
    getAll: (skip: number, limit: number) =>
      `${BASE_URL}/data-sources/all?skip=${skip}&limit=${limit}`,
    getById: (id: string) => `${BASE_URL}/data-sources/${id}`,
    create: `${BASE_URL}/data-sources`,
    update: (id: string) => `${BASE_URL}/data-sources/${id}`,
    delete: (id: string) => `${BASE_URL}/data-sources/${id}`,
  },
  data_source_type: {
    getAll: (skip: number, limit: number) =>
      `${BASE_URL}/data-source-type/all?skip=${skip}&limit=${limit}`,
    getById: (id: string) => `${BASE_URL}/data-source-type/${id}`,
    create: `${BASE_URL}/data-source-type`,
    update: (id: string) => `${BASE_URL}/data-source-type/${id}`,
    delete: (id: string) => `${BASE_URL}/data-source-type/${id}`,
  },
};
