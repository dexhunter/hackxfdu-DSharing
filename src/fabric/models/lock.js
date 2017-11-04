/**
 * Place an order for a house
 * @param {org.acme.lock.TransferOwnership} transferOwnership - the TransferOwnership transaction
 * @transaction
 */
function transferOwnership(transferOwnership) {
  console.log('lock ownership transfering');
  if (transferOwnership.oldOwner != transferOwnership.lock.masterKey) {
    throw new Error("invalid lock!");
  }
  //give lock admission to tenant
  if (transferOwnership.flag) {
  	if (transferOwnership.lock.enable == true) {
    	throw new Error("the lock is being used!");
  	}
  	transferOwnership.lock.userKey = transferOwnership.newOwner;
  	transferOwnership.lock.enable = true;
    transferOwnership.lock.status = true;
  }
  else {
    //return the lock ownership to renter
    transferOwnership.lock.enable = false;
    transferOwnership.lock.status = true;
  }
  if (transferOwnership.lock.unlockTimes) {
    transferOwnership.lock.unlockTimes = 0;
  }
  return getParticipantRegistry('org.acme.lock.Lock')
  		.then(function (lockRegistry) {
    		return lockRegistry.update(transferOwnership.lock)		
  		});
}

/**
 * Place an order for a house
 * @param {org.acme.lock.LockOrder} lockOrder - the LockOrder transaction
 * @transaction
 */
function lockOrder(lockOrder) {
  console.log('connecting lock...');
  if (lockOrder.newOwner.tenantId != lockOrder.lock.userKey.tenantId || lockOrder.lock.enable == false) {
    throw new Error("admission denied");
  }
  //handle LOCK or UNLOCK command
  if (lockOrder.order.oneOrder == 'LOCK') {
  	lockOrder.lock.status = true;
  }
  else {
    lockOrder.lock.status = false;
    if (lockOrder.lock.unlockTimes >= 0) {
      lockOrder.lock.unlockTimes += 1;
    }
  }
  
  return getParticipantRegistry('org.acme.lock.Lock')
  		.then(function (lockRegistry) {
    		return lockRegistry.update(lockOrder.lock)		
  		}); 		
}


