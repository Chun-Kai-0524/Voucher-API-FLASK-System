"""
Batch Service
批次操作服務（加分項）

使用 asyncio 處理大量資料
"""
import asyncio
from typing import List, Dict, Any, Tuple
from concurrent.futures import ThreadPoolExecutor

from sqlalchemy.orm import Session

from app.models.voucher import Voucher
from app.repositories.voucher_repository import VoucherRepository
from app.services.voucher_service import VoucherService


class BatchService:
    """批次操作服務"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = VoucherRepository(db)
        self.service = VoucherService(db)
    
    async def batch_create_vouchers(
        self,
        vouchers_data: List[Dict[str, Any]],
        chunk_size: int = 100
    ) -> Dict[str, Any]:
        """
        批次創建優惠券（使用 asyncio）
        
        Args:
            vouchers_data: 優惠券資料列表
            chunk_size: 每批次處理的數量
            
        Returns:
            Dict: 執行結果統計
        """
        total = len(vouchers_data)
        success_count = 0
        failure_count = 0
        failures = []
        
        # 分批處理
        chunks = [
            vouchers_data[i:i + chunk_size]
            for i in range(0, len(vouchers_data), chunk_size)
        ]
        
        # 使用 asyncio 並行處理各批次
        tasks = []
        for chunk_index, chunk in enumerate(chunks):
            task = self._process_create_chunk(
                chunk,
                chunk_index * chunk_size,
                failures
            )
            tasks.append(task)
        
        # 等待所有任務完成
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 統計結果
        for result in results:
            if isinstance(result, Exception):
                failure_count += chunk_size
            elif isinstance(result, int):
                success_count += result
        
        failure_count = total - success_count
        
        # 提交事務
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Batch create failed: {str(e)}")
        
        return {
            'success_count': success_count,
            'failure_count': failure_count,
            'total': total,
            'failures': failures
        }
    
    async def _process_create_chunk(
        self,
        chunk: List[Dict[str, Any]],
        start_index: int,
        failures: List[Dict[str, Any]]
    ) -> int:
        """
        處理單一批次的創建（展示 asyncio 用法）
        
        Returns:
            int: 成功創建的數量
        """
        success = 0
        
        # 在執行緒池中執行資料庫操作（避免阻塞）
        loop = asyncio.get_event_loop()
        
        with ThreadPoolExecutor() as executor:
            futures = []
            
            for index, data in enumerate(chunk):
                future = loop.run_in_executor(
                    executor,
                    self._create_single_voucher,
                    data,
                    start_index + index,
                    failures
                )
                futures.append(future)
            
            # 等待所有創建完成
            results = await asyncio.gather(*futures, return_exceptions=True)
            
            # 統計成功數量
            for result in results:
                if result is True:
                    success += 1
        
        return success
    
    def _create_single_voucher(
        self,
        data: Dict[str, Any],
        index: int,
        failures: List[Dict[str, Any]]
    ) -> bool:
        """
        創建單一優惠券
        
        Returns:
            bool: 是否成功
        """
        try:
            self.service._validate_voucher_data(data)
            self.repository.create(data)
            return True
        except Exception as e:
            failures.append({
                'index': index,
                'error': str(e),
                'data': data
            })
            return False
    
    async def batch_update_vouchers(
        self,
        updates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        批次更新優惠券
        
        Args:
            updates: 更新資料列表，每項包含 'id' 和 'data'
            
        Returns:
            Dict: 執行結果統計
        """
        total = len(updates)
        success_count = 0
        failures = []
        
        # 使用 asyncio 並行處理
        loop = asyncio.get_event_loop()
        
        with ThreadPoolExecutor() as executor:
            tasks = []
            
            for index, update_item in enumerate(updates):
                task = loop.run_in_executor(
                    executor,
                    self._update_single_voucher,
                    update_item,
                    index,
                    failures
                )
                tasks.append(task)
            
            # 等待所有更新完成
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 統計成功數量
            for result in results:
                if result is True:
                    success_count += 1
        
        failure_count = total - success_count
        
        # 提交事務
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Batch update failed: {str(e)}")
        
        return {
            'success_count': success_count,
            'failure_count': failure_count,
            'total': total,
            'failures': failures
        }
    
    def _update_single_voucher(
        self,
        update_item: Dict[str, Any],
        index: int,
        failures: List[Dict[str, Any]]
    ) -> bool:
        """
        更新單一優惠券
        
        Returns:
            bool: 是否成功
        """
        try:
            voucher_id = update_item['id']
            data = update_item['data']
            
            voucher = self.repository.get_by_id(voucher_id)
            if not voucher:
                raise ValueError(f"Voucher {voucher_id} not found")
            
            self.service._validate_update_data(voucher, data)
            self.repository.update(voucher, data)
            return True
        except Exception as e:
            failures.append({
                'id': update_item.get('id'),
                'error': str(e)
            })
            return False

