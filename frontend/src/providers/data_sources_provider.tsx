import { createContext, PropsWithChildren, ReactNode } from "react";
import { useFetchAllData } from "../hooks/useFetchAllData";
import { DataSourceSchema, dataSourceSchema } from "@/types/data_source.type";
import { endpoints } from "@/utils/endpoints";

interface DataContextProps<T> {
  data: T | undefined;
  isLoading: boolean;
  error: any;
}

export const DataContext = createContext(
  {} as DataContextProps<DataSourceSchema[]>
);

interface DataProviderProps {
  children: ReactNode;
}

const DataProvider = ({ children }: PropsWithChildren<{}>) => {
  const { data, isLoading, error } = useFetchAllData(
    dataSourceSchema,
    endpoints.data_source.getAll(0, 100)
  );

  return (
    <DataContext.Provider value={{ data, isLoading, error }}>
      {children}
    </DataContext.Provider>
  );
};

export default DataProvider;
