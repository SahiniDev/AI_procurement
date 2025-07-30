import axios from "axios";

export interface OrderLine {
  description:    string;
  unit_price:     number;
  amount:         number;
  unit:           string;
  total_price:    number;
  commodity_group:string;
}

export interface ExtractResponse {
  vendor?: string;
  vat?:    string;
  total?:  number;
  order_lines?: OrderLine[];
  error?:  string;
}

export const extractPdf = async (file: File): Promise<ExtractResponse> => {
  const form = new FormData();
  form.append("file", file);

  const { data } = await axios.post<ExtractResponse>(
    "http://localhost:5000/extract",
    form,
    { headers: { "Content-Type": "multipart/form-data" } }
  );
  return data;
};

export interface Entry {
  id: number;
  filename: string;
  extracted_data: any;
  status: number; // 0: Open, 1: In Progress, 2: Closed
}

export const getAllEntries = async (): Promise<Entry[]> => {
  const { data } = await axios.get<Entry[]>("http://localhost:5000/entries");
  return data;
};

export const updateEntryStatus = async (entryId: number, status: number): Promise<void> => {
  if (![0, 1, 2].includes(status)) {
    throw new Error("Invalid status. Valid values are 0 (Open), 1 (In Progress), 2 (Closed).");
  }

  await axios.put(`http://localhost:5000/entries/${entryId}/${status}`);
};