class DataHandler:
    @staticmethod
    def group_by_eo(data):
        """Группирует данные по EO."""
        grouped_data = {}
        for record in data:
            eo = record["eo"]
            if eo not in grouped_data:
                grouped_data[eo] = []
            grouped_data[eo].append(record)
        return grouped_data
