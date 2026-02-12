/** Status do fluxo de atendimento do Lead 
 */
export type LeadStatus = 'NEW' | 'SENT_HELLO' | 'REPLIED' | 'BLACKLIST';

/** Tipo de tecnologia da linha telefônica 
 */
export type PhoneType = 'mobile' | 'landline';

export interface Lead {
  readonly id: number;
  business_name: string;
  phone_raw: string;
  phone_clean: string;
  lead_type: PhoneType;
  status: LeadStatus;
  
  /** ISO 8601 format: YYYY-MM-DDTHH:mm:ssZ */
  createdAt: Date | string; 
}