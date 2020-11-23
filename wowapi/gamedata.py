class GameData():

    # Get list of all realms in region
    def get_realm_index(self, region, namespace, **filters):
        
        filters['namespace'] = namespace
        return self.get_resource('/data/wow/connected-realm/index', region, **filters)
    
    # Get Realm by ID
    def get_connected_realm(self, region, namespace, id, **filters):
        """
        Data Connected Realm API - Returns a connected realm by id
        """
        filters['namespace'] = namespace
        return self.get_resource('data/wow/connected-realm/{0}', region, *[id], **filters)

    def get_auctions(self, last_modified, region, namespace, connected_realm_id, **filters):
        """
        Auction House API - Returns all active auctions for a connected realm
        """
        filters['namespace'] = namespace
        return self.get_resource(
            'data/wow/connected-realm/{0}/auctions',
            region,
            *[connected_realm_id],
            **filters
        )