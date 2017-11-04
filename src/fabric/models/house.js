/**
 * Place an order for a house
 * @param {org.acme.items.RentHouse} rentHouse - the RentHouse transaction
 * @transaction
 */
function rentHouse(rentHouse) {
  console.log('rent house');
  if (rentHouse.house.owner != rentHouse.renter) {
    throw new Error("invalid house!");
  }
  if (rentHouse.house.gas > 0 ) {
    throw new Error("The house haven't been returned");
  }
  if (rentHouse.tenant.balance < rentHouse.payment) {
    throw new Error("Don't have enough money!");
  }
  rentHouse.house.user = rentHouse.tenant;
  rentHouse.house.gas = rentHouse.payment;
  
  return getParticipantRegistry('org.acme.roles.Tenant')
  		.then(function (roleRegistry) {
    		rentHouse.tenant.balance -= rentHouse.payment;
    		return roleRegistry.update(rentHouse.tenant);
  		})
        .then(function () {
            return getAssetRegistry('org.acme.items.House');
        })
  		.then(function (assetRegistry) {
    		return assetRegistry.update(rentHouse.house);
  		});
  		
}

/**
 * Place an order for a house
 * @param {org.acme.items.ReturnHouse} returnHouse - the ReturnHouse transaction
 * @transaction
 */
function returnHouse(returnHouse) {
  console.log('return house');
  if (returnHouse.house.owner != returnHouse.renter) {
    throw new Error("invalid house!");
  }
  if (returnHouse.house.gas > 0 ) {
    returnHouse.tenant.balance += returnHouse.house.gas;
  }
  returnHouse.house.user = returnHouse.tenant;
  returnHouse.house.gas = 0;
  return getAssetRegistry('org.acme.items.House')
        .then(function (assetRegistry) {
            return assetRegistry.update(returnHouse.house);
        })
  		.then(function () {
    		return getParticipantRegistry('org.acme.roles.Tenant');
  		})
  		.then(function (roleRegistry) {
    		return roleRegistry.update(returnHouse.tenant);
  		});
 
}

/**
 * send money to renter periodly
 * @param {org.acme.items.SendGas} sendGas - the sendGas transaction (to record time)
 * @transaction
 */
function sendGas(sendGas) {
  console.log('send money');
  if (sendGas.house.owner != sendGas.renter) {
    throw new Error("invalid house!");
  }
  if (sendGas.house.gas < sendGas.eachSend ) {
    sendGas.renter.balance += sendGas.house.gas;
    sendGas.house.gas = 0;
  }
  else {
    sendGas.renter.balance += sendGas.eachSend;
    sendGas.house.gas -= sendGas.eachSend;
  }
  return getAssetRegistry('org.acme.items.House')
        .then(function (assetRegistry) {
            return assetRegistry.update(sendGas.house);
        })
  		.then(function () {
    		return getParticipantRegistry('org.acme.roles.Renter');
  		})
  		.then(function (roleRegistry) {
    		return roleRegistry.update(sendGas.renter);
  		});
 
}
