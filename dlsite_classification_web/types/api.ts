/**
 * API Type Definitions
 * Single Responsibility: Define all API-related types
 */

export interface WorkInfo {
  code: string
  title: string
  company: string
  company_id: string
  main_image_path?: string
  genre?: string[]
  work_format?: string
  file_format?: string
  sale_date?: string
  my_rating?: string | number
  my_collection?: string | boolean
  [key: string]: unknown
}

export interface WorksResponse {
  works: WorkInfo[]
  total: number
  companies: string[]
  genres: string[]
  work_formats?: string[]
  file_formats?: string[]
}

export interface GenreInfo {
  name: string
  count: number
}

export interface GenresResponse {
  genres: GenreInfo[]
}

export interface CollectionsResponse {
  collections: string[]
}

export interface FilterParams {
  search?: string
  company?: string
  collection?: string
  my_collection?: boolean
  my_rating?: number | string
  work_format?: string
  file_format?: string
  tags?: string
  tag_mode?: 'AND' | 'OR'
  sort?: string
  limit?: number
  offset?: number
}

export interface UserDataUpdate {
  my_rating?: number
  my_collection?: string
}
