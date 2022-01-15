export interface SearchLocations {
  id: number;
  name: string;
  url: string;
}

export interface SearchTerms {
  id: number;
  term: string;
}

export interface Search {
  id: number;
  name: string;
  description: string;
  is_rss: boolean;
  search_locations: SearchLocations[];
  search_terms: SearchTerms[];
}

export interface SearchMenu {
  id: number;
  name: string;
}
