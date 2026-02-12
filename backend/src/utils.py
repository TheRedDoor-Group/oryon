import re

class PhoneCleaner:
    def clean(self, phone_raw):
        """
            Recebe um telefone bruto e retorna:
            - valid: True/False
            - type: 'mobile', 'landline', 'unknown'
            - clean_number: 5511999998888 (apenas números)
        """
        if not phone_raw:
            return {"valid": False, "type": "empty", "clean_number": None}

        # Remove tudo que não é dígito
        nums = re.sub(r'\D', '', str(phone_raw))

        # Remove zero à esquerda (comum em SP: 011...)
        if nums.startswith('0'):
            nums = nums[1:]
        
        # Se tiver 10 ou 11 dígitos, adiciona o DDI 55
        if len(nums) in [10, 11]:
            nums = '55' + nums
            
        # Regex para Celular BR (DDD + 9 + 8 digitos)
        if re.match(r"^55[1-9]{2}9[0-9]{8}$", nums):
            return {"valid": True, "type": "mobile", "clean_number": nums}
        
        # Regex para Fixo BR (DDD + [2-5] + 7 digitos)
        elif re.match(r"^55[1-9]{2}[2-5][0-9]{7}$", nums):
            return {"valid": True, "type": "landline", "clean_number": nums}
            
        return {"valid": False, "type": "unknown", "clean_number": nums}